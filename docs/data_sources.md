# 数据来源、时间与口径

## 历史商品与评论

- 数据集：Amazon Reviews 2023 / All_Beauty。
- 发布方：McAuley Lab, UC San Diego。
- 项目主页：https://amazon-reviews-2023.github.io/main.html
- 商品原始数据：https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_All_Beauty.jsonl.gz
- 评论原始数据：https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/All_Beauty.jsonl.gz
- 项目取得日期：2026-10-20 UTC；原始文件校验值记录在本地项目的数据来源清单中。
- 关键词初筛得到 1,892 件候选商品和 5,927 条关联评论；清洗后分析使用 5,852 条有效评论。
- 评论最晚日期为 2023-07-28 UTC。商品与评论通过父商品 ID 关联。

## 当前商品榜单与详情

- 来源：Amazon 美国站一次榜单网页快照及后续商品详情页核对。
- 榜单快照时间：2026-10-21 00:49:37（北京时间）。
- 初始榜单 30 条；经范围核对，28 件纳入价格描述、1 件排除、1 件待核对。
- 10 件详情页商品按价格层选择：低价 5 件、中价 2 件、高价 3 件；记录商品链接、页面规格、商家文案和核对时间。
- 页面展示价与详情核对可能来自不同时间或页面币种设置；本项目价格比较使用榜单快照中的美元价格。

## 文件口径

| 文件 | 内容 | 注意事项 |
|---|---|---|
| `data/outputs/historical_spec_frequency_draft.csv` | 历史标题初筛商品的规格候选频次 | 不是人工完整审核结果、销量份额或市场占比 |
| `data/outputs/historical_review_product_sample.csv` | 16 件历史重点商品的选样信息 | 按评论量和低星反馈选样，不是随机选商品 |
| `data/outputs/historical_review_theme_summary.csv` | 95 条定向阅读评论的主要主题汇总 | 每条只计一个主要主题；低星优先，不能估总体差评率 |
| `data/outputs/current_listing_price_scope.csv` | 30 条当前榜单的范围判断和价格 | 单次快照；不代表全市场、成交价或长期价格 |
| `data/outputs/current_competitor_detail_comparison.csv` | 10 件详情页对比 | 页面宣称与实测结果分开解释 |
| `data/outputs/issue_to_competitor_actions.csv` | 历史问题、当前供给和候选测试方向对照 | 两个时期按问题主题对照，不做商品 ID 连接 |

## 数据使用说明

仓库保留来源链接和汇总结果，不再分发原始评论全集及逐条评论原文。运行下载脚本后，原始数据留在本地 `data/raw/`；清洗后的行级数据也留在本地。公开展示时请同时保留数据集来源、采集日期、筛选口径和上述限制。
