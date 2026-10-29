# Amazon 美国站穿戴甲竞品分析与选品方案

一个面向产品开发与跨境电商选品的个人分析项目：将历史消费者评论转成可追溯的问题线索，再与当前在售商品的规格和页面信息对照，形成待验证的商品概念与测试计划。

## 项目结论

当前优先建议验证**日常贴合型短椭圆套装**：以 32 片／16 种尺码为打样基准，加入尺码编号与宽度选码说明，重点测试宽拇指、小指和甲床弧度适配；胶水与胶贴表现分别测试。**设计升级型短杏仁款**作为备选，聚焦图案耐磨和页面图片与实物一致性。

这两项是由数据提出的产品假设。项目尚未打样、试戴、询得供应商报价或进行销售测试，不能称为已验证的创新、市场需求或经营成果。方案和验证项见[候选商品方案](docs/product_concepts.md)。

## 主要分析结果

- 历史数据来自 Amazon Reviews 2023 / All_Beauty。关键词初筛得到 1,892 件候选商品及 5,927 条关联评论；清洗后分析使用 5,852 条有效评论。
- 依据标题规则，1,892 件商品中有 1,079 件标题明确、616 件排除、197 件待核对。标题明确纳入是程序初筛结果，尚不代表 1,079 件都已人工确认。
- 从 16 件历史商品的 207 条评论中，按商品和星级分层抽取 95 条人工阅读，抽样优先覆盖低星评论。厚薄与耐用、尺寸与贴合、粘性与脱落分别是 22、16、16 条评论的**主要主题**。
- 当前竞品为 2026-10-21（北京时间）采集的榜单快照。30 条中 28 件纳入价格描述，页面展示价为 4.48—17.99 美元，中位数 12.99 美元。
- 从 28 件中按价格层抽取 10 件详情核对：7 件明确列出 12—21 种尺码；9 件明确描述至少一种粘贴方式；4 件明确写出材质。页面上的佩戴时长和耐用性文字属于商家宣称，未由本项目实测。

## 分析流程

1. 定义研究边界：Amazon 美国站家用成品穿戴甲套装。
2. 检查商品、评论和当前榜单数据的缺失、重复、标识符、价格和时间口径。
3. 对历史商品标题作初筛，提取规格候选，并按评论数量和低星反馈挑选重点商品。
4. 按商品和星级分层抽取评论，人工阅读、标注主要主题与情感，并保留原始索引作回查依据。
5. 从当前榜单核对 28 件目标商品的价格，再分层检查 10 件详情页。
6. 按问题主题对照历史反馈与当前页面供给，不将不同时期商品按 ID 强行连接。
7. 形成两个待验证产品概念，写出取舍、待验证问题和样品测试方向。

详细流程见[项目方法与发现](docs/project_methodology.md)、[候选商品方案](docs/product_concepts.md)、[第 1—7 节项目复盘](docs/project_retrospective.md)、[产品开发方向完整汇报稿](docs/leader_briefing.md)、[数据来源与口径](docs/data_sources.md)、[Agent 协作记录](docs/agent_workflow.md)和[Power BI 页面设计](docs/powerbi_dashboard.md)。

## 仓库内容

```text
.
├── README.md
├── requirements.txt
├── docs/
│   ├── agent_workflow.md
│   ├── data_sources.md
│   ├── leader_briefing.md
│   ├── powerbi_dashboard.md
│   ├── product_concepts.md
│   ├── project_methodology.md
│   └── project_retrospective.md
├── scripts/
│   ├── analyze_current_snapshot.py
│   ├── download_dataset.py
│   ├── prepare_candidate_data.py
│   ├── sample_reviews.py
│   ├── screen_historical_products.py
│   └── summarize_review_themes.py
├── data/
│   ├── outputs/       # 汇总结果与当前竞品分析表
│   └── templates/     # 人工评论编码表空模板
└── assets/            # 价格分布图
```

## 如何复现

需要 Python 3.10 或更新版本。

```bash
pip install -r requirements.txt
python scripts/download_dataset.py
python scripts/prepare_candidate_data.py
python scripts/screen_historical_products.py
```

原始数据和含逐条评论文本的中间表保存在本地 `data/raw/`、`data/processed/` 与 `data/private/`，由 `.gitignore` 排除。`sample_reviews.py` 需要你先把清洗后的重点商品评论整理为 `data/private/focus_product_reviews.csv`（保留源表行号）；`summarize_review_themes.py` 需要人工核验后的 `data/private/review_annotations.csv`。这两类行级文件不会提交到仓库。空白模板位于 `data/templates/review_annotation_template.csv`。

当前竞品结果是有日期的网页快照。再次采集时应另存新的日期版本并重新核对商品范围；不要覆盖旧快照后把不同日期误作连续趋势。

## 工具与 Agent 协作

Python（pandas）用于数据清洗、关联、抽样和汇总；Excel 用于商品核对及评论人工编码；Power BI 用于呈现评论主题和情感分布。Agent 协助拆分分析任务、编写和调试脚本、整理检查清单；人工确认分析口径、回查原文并判断产品方案。

## 数据边界

95 条评论是低星优先的定向分层阅读样本，不能用来估计全部消费者的差评率。历史商品的规格频次来自标题初筛，不能当作市场份额。当前价格来自 28 件榜单快照，不代表全站价格带或成交价。历史评论商品与当前竞品不是同一批商品；第 6 节按问题主题作对照，不是同款商品的时间比较。

仓库保留汇总统计、竞品对比、分析代码和数据来源说明。原始评论全文及逐条人工标注表没有放入仓库；它们可从数据来源按文档步骤重新处理。当前榜单快照包含公开商品链接与价格，只代表注明日期的一次采集。
