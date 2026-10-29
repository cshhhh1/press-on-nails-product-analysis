"""Aggregate manually coded review themes without exporting review text."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "private" / "review_annotations.csv"
OUTPUT = ROOT / "data" / "outputs" / "historical_review_theme_summary_rebuilt.csv"
THEMES = ["厚薄与耐用", "尺寸与贴合", "粘性与脱落", "外观设计", "包装与配件", "颜色与图片一致性"]


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Place the manually checked annotation table at {SOURCE}. It stays local and is ignored by Git."
        )
    data = pd.read_csv(SOURCE, encoding="utf-8-sig")
    required = {"源表原始索引", "父商品ID", "问题或满意点类别", "情感判断"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    data = data.drop_duplicates("源表原始索引").copy()
    results = []
    for theme in THEMES:
        subset = data[data["问题或满意点类别"].eq(theme)]
        sentiment = subset["情感判断"].fillna("")
        results.append({
            "问题主题": theme,
            "已读样本评论数": subset["源表原始索引"].nunique(),
            "负面评论数": subset.loc[sentiment.eq("负面"), "源表原始索引"].nunique(),
            "混合评论数": subset.loc[sentiment.eq("混合"), "源表原始索引"].nunique(),
            "正面评论数": subset.loc[sentiment.eq("正面"), "源表原始索引"].nunique(),
            "中性或待判断数": subset.loc[sentiment.isin(["中性", "待判断"]), "源表原始索引"].nunique(),
            "涉及历史商品数": subset["父商品ID"].nunique(),
            "统计口径": "人工定向阅读样本；每条评论只计一个主要主题",
        })
    summary = pd.DataFrame(results)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    print(summary.to_string(index=False))
    print(f"仅输出汇总统计：{OUTPUT}")


if __name__ == "__main__":
    main()
