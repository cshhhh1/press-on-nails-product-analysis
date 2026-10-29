"""Recalculate the included-listing price summary and create a histogram."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "outputs" / "current_listing_price_scope.csv"
SUMMARY = ROOT / "data" / "outputs" / "current_snapshot_summary.json"
FIGURE = ROOT / "assets" / "current_competitor_price_distribution.png"


def main() -> None:
    data = pd.read_csv(SOURCE, encoding="utf-8-sig")
    status = data["修正纳入状态"].fillna("").astype(str)
    included = data[status.eq("纳入")].copy()
    included["快照价格_美元"] = pd.to_numeric(included["快照价格_美元"], errors="coerce")
    prices = included["快照价格_美元"].dropna()
    if prices.empty:
        raise ValueError("No included products have a numeric snapshot price.")
    summary = {
        "snapshot_time_beijing": str(data["快照采集时间_北京时间"].dropna().iloc[0]),
        "listing_rows": int(len(data)),
        "included_products": int(len(included)),
        "excluded_products": int(status.eq("排除").sum()),
        "needs_review_products": int(status.str.contains("待核对|不确定", regex=True).sum()),
        "priced_included_products": int(prices.size),
        "min_usd": round(float(prices.min()), 2),
        "median_usd": round(float(prices.median()), 2),
        "mean_usd": round(float(prices.mean()), 2),
        "max_usd": round(float(prices.max()), 2),
        "scope_note": "One dated ranking snapshot; not the entire market or transaction prices.",
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    FIGURE.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5), dpi=150)
    plt.hist(prices, bins=8, color="#3978C5", edgecolor="white")
    plt.title("Current listing price distribution (included snapshot sample)")
    plt.xlabel("Displayed price (USD)")
    plt.ylabel("Number of listings")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGURE, bbox_inches="tight")
    plt.close()

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Saved histogram: {FIGURE}")


if __name__ == "__main__":
    main()
