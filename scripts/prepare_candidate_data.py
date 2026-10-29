"""Extract keyword-matched press-on nail candidates from the downloaded public files.

Outputs contain row-level review text and are written only under ignored data/processed/.
This is a candidate extraction step, not the project's final manual review or cleaned sample.
"""

from __future__ import annotations

import csv
import gzip
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)
META = RAW / "All_Beauty_metadata.jsonl.gz"
REVIEWS = RAW / "All_Beauty_reviews.jsonl.gz"
PRODUCT_PATTERN = re.compile(
    r"\b(?:press[ -]?on nails?|fake nails?|false nails?|artificial nails?|acrylic nail tips?|full cover nail tips?|glue[ -]?on nails?)\b",
    re.I,
)


def records(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run scripts/download_dataset.py first.")
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if line.strip():
                item = json.loads(line)
                item["_source_row"] = line_number - 1
                yield item


def dump_csv(path: Path, fields: list[str], rows) -> int:
    count = 0
    with path.open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            count += 1
    return count


def main() -> None:
    product_fields = [
        "source_row", "parent_asin", "title", "price", "average_rating", "rating_number",
        "store", "features", "description", "details",
    ]
    candidate_products = []
    product_ids: set[str] = set()
    for item in records(META):
        title = item.get("title") or ""
        parent_id = item.get("parent_asin") or ""
        if PRODUCT_PATTERN.search(title) and parent_id:
            product_ids.add(parent_id)
            candidate_products.append({
                "source_row": item["_source_row"],
                "parent_asin": parent_id,
                "title": title,
                "price": item.get("price"),
                "average_rating": item.get("average_rating"),
                "rating_number": item.get("rating_number"),
                "store": item.get("store") or "",
                "features": json.dumps(item.get("features") or [], ensure_ascii=False),
                "description": json.dumps(item.get("description") or [], ensure_ascii=False),
                "details": json.dumps(item.get("details") or {}, ensure_ascii=False),
            })

    product_path = OUT / "candidate_products.csv"
    product_count = dump_csv(product_path, product_fields, candidate_products)

    review_fields = [
        "source_row", "parent_asin", "asin", "rating", "timestamp", "verified_purchase",
        "helpful_vote", "title", "text",
    ]
    review_counts: Counter[str] = Counter()

    def matched_reviews():
        for item in records(REVIEWS):
            parent_id = item.get("parent_asin") or ""
            if parent_id not in product_ids:
                continue
            review_counts[parent_id] += 1
            yield {
                "source_row": item["_source_row"],
                "parent_asin": parent_id,
                "asin": item.get("asin") or "",
                "rating": item.get("rating"),
                "timestamp": item.get("timestamp", item.get("sort_timestamp")),
                "verified_purchase": item.get("verified_purchase"),
                "helpful_vote": item.get("helpful_vote", item.get("helpful_votes")),
                "title": item.get("title") or "",
                "text": item.get("text") or "",
            }

    review_count = dump_csv(OUT / "candidate_reviews_raw.csv", review_fields, matched_reviews())
    stats = {
        "keyword_candidate_product_rows": product_count,
        "distinct_candidate_parent_asins": len(product_ids),
        "linked_review_rows_before_cleaning": review_count,
        "candidate_products_with_reviews": len(review_counts),
        "important": "These are keyword candidates and linked raw reviews; inspect/clean before analysis. Row-level review text stays local.",
    }
    (OUT / "candidate_extract_summary.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
