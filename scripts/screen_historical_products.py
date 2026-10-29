"""Create a title/details based first-pass product screening worksheet.

All predicted fields are suggestions for human review; they must not be treated as
confirmed product attributes. The worksheet is local and ignored by Git.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "processed" / "candidate_products.csv"
OUTPUT = ROOT / "data" / "private" / "historical_product_screening.csv"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


def extract(row: pd.Series) -> pd.Series:
    title = str(row.get("title", "") or "")
    parts = [str(row.get(col, "") or "") for col in ("features", "description", "details")]
    text = " ".join([title, *parts]).lower()
    positive = bool(re.search(r"press[ -]?on nails?|false nails?|fake nails?|artificial nails?|nail tips?", text))
    accessory = bool(re.search(r"\b(glue|adhesive|tabs?|lamp|polish|gel|remover|file|brush|stickers?)\b", title.lower()))
    set_hint = bool(re.search(r"\b(set|kit|pcs?|pieces?|count|full cover)\b", text))
    if positive and not accessory and set_hint:
        group = "疑似成品套装"
    elif not positive and accessory:
        group = "明显不相关_需抽查"
    else:
        group = "待核对"
    count = re.search(r"\b(\d{1,3})\s*(?:pcs?|pieces?|count)\b", text)
    lengths = [x for x in ("extra short", "short", "medium", "long") if re.search(r"\b" + x + r"\b", text)]
    shapes = [x for x in ("almond", "square", "coffin", "oval", "stiletto", "round") if re.search(r"\b" + x + r"\b", text)]
    materials = [x for x in ("abs", "acrylic", "gel", "plastic") if re.search(r"\b" + x + r"\b", text)]
    return pd.Series({
        "程序初筛": group,
        "片数候选": count.group(1) if count else "",
        "长度候选": "、".join(lengths),
        "形状候选": "、".join(shapes),
        "材质候选": "、".join(materials),
        "胶水胶贴候选": "有提及" if re.search(r"\b(glue|adhesive tabs?)\b", text) else "",
        "可复用候选": "有提及" if re.search(r"\breusab(le|ility)\b", text) else "",
    })


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing {SOURCE}. Run scripts/prepare_candidate_data.py first.")
    products = pd.read_csv(SOURCE, encoding="utf-8-sig").fillna("")
    suggestions = products.apply(extract, axis=1)
    result = pd.concat([products, suggestions], axis=1)
    for column in (
        "是否纳入_人工", "排除原因_人工", "片数_人工", "长度_人工", "形状_人工",
        "材质_人工", "是否附胶水胶贴_人工", "是否标称可复用_人工", "规格证据_人工",
    ):
        result[column] = ""
    result.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    print(f"输出 {len(result):,} 行人工复核工作表：{OUTPUT}")
    print(result["程序初筛"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
