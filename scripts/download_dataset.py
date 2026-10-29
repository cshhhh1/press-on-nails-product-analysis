"""Download the public Amazon Reviews 2023 All_Beauty files to ignored data/raw/."""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
SOURCES = {
    "All_Beauty_reviews.jsonl.gz": "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/All_Beauty.jsonl.gz",
    "All_Beauty_metadata.jsonl.gz": "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_All_Beauty.jsonl.gz",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(name: str, url: str) -> dict[str, object]:
    target = RAW / name
    partial = RAW / (name + ".part")
    if target.exists() and target.stat().st_size:
        return {"file": f"data/raw/{name}", "url": url, "bytes": target.stat().st_size, "sha256": sha256(target)}

    for attempt in range(1, 7):
        offset = partial.stat().st_size if partial.exists() else 0
        headers = {"Range": f"bytes={offset}-"} if offset else {}
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(20, 120)) as response:
                response.raise_for_status()
                if offset and response.status_code != 206:
                    partial.unlink(missing_ok=True)
                    offset = 0
                mode = "ab" if offset else "wb"
                with partial.open(mode) as output:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            output.write(chunk)
            partial.replace(target)
            return {"file": f"data/raw/{name}", "url": url, "bytes": target.stat().st_size, "sha256": sha256(target)}
        except (requests.RequestException, OSError):
            if attempt == 6:
                raise
            time.sleep(min(2**attempt, 20))
    raise RuntimeError(f"Could not download {name}")


if __name__ == "__main__":
    manifest = {
        "dataset": "Amazon Reviews 2023 / All_Beauty",
        "publisher": "McAuley Lab, UC San Diego",
        "homepage": "https://amazon-reviews-2023.github.io/main.html",
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": [download(name, url) for name, url in SOURCES.items()],
        "note": "Raw files stay in ignored data/raw/ and are not committed.",
    }
    path = ROOT / "data" / "raw" / "source_manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
