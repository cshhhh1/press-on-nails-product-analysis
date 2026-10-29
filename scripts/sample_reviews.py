"""Draw a low-star-prioritized, per-product review reading sample.

Prepare data/private/focus_product_reviews.csv first. Required columns are
parent_asin, source_row, rating, title, and text. This file contains review text
and is intentionally excluded from Git.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "private" / "focus_product_reviews.csv"
OUTPUT = ROOT / "data" / "private" / "review_reading_sample.csv"


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Create {SOURCE} from the cleaned reviews for the selected products first."
        )
    data = pd.read_csv(SOURCE, encoding="utf-8-sig")
    required = {"parent_asin", "source_row", "rating", "title", "text"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    data["rating"] = pd.to_numeric(data["rating"], errors="coerce")
    data = data.dropna(subset=["parent_asin", "source_row", "rating"]).copy()
    data["star_band"] = pd.cut(
        data["rating"], bins=[0, 2, 3, 5], labels=["low", "middle", "high"], include_lowest=True
    )

    samples = []
    for _, group in data.groupby("parent_asin", sort=True, observed=True):
        chosen = []
        for band, quota in (("low", 3), ("middle", 1), ("high", 2)):
            part = group[group["star_band"].astype(str).eq(band)]
            if not part.empty:
                chosen.append(part.sample(n=min(quota, len(part)), random_state=23))
        selected = pd.concat(chosen).drop_duplicates("source_row") if chosen else group.iloc[0:0]
        target = min(6, len(group))
        if len(selected) < target:
            remaining = group[~group["source_row"].isin(selected["source_row"])]
            selected = pd.concat([
                selected,
                remaining.sample(n=target - len(selected), random_state=24),
            ])
        samples.append(selected)

    result = pd.concat(samples, ignore_index=True).sort_values(
        ["parent_asin", "source_row"]
    ).reset_index(drop=True)
    result.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    print(f"抽取 {len(result)} 条，覆盖 {result['parent_asin'].nunique()} 件商品")
    print("按星级：", result["rating"].value_counts().sort_index().to_dict())
    print(f"行级评论文本仅保存在本地：{OUTPUT}")


if __name__ == "__main__":
    main()
