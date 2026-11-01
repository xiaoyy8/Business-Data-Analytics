# Superstore 零售业务经营诊断与用户价值分析

《商业数据分析》期末大作业 · 主题：**Tableau Superstore** 零售数据集

用 Python 完成「合规获取 → 清洗治理 → 9 类商业模型 → 16 种图表模板复现 → 交互式大屏 → 论文」的端到端分析，
全部结论可由 4 个 Jupyter Notebook 一键复现。

---

## 1. 交付物清单

| 类别 | 位置 | 说明 |
|---|---|---|
| 期末论文 | `docs/Superstore零售业务经营诊断与用户价值分析.docx` | 按教师模板填写，38 页 / 约 2.36 万字符（中文 1.18 万），27 张图、7 张编号表 |
| 论文 PDF（预览） | `docs/Superstore论文预览.pdf` | 与 docx 同源导出，用于快速翻阅 |
| 代码（Notebook） | `notebooks/01~04.ipynb` | 4 个 notebook，共 131 个 cell，已带执行输出 |
| 图表 | `outputs/figures/` | 27 张 PNG，200 dpi，命名 `figXX_中文名称.png` |
| 结果表 | `outputs/tables/` | 14 个 CSV/JSON，含 RFM、聚类、同期群、关联规则、预测、模型评估 |
| 交互大屏 | `outputs/dashboard/superstore_dashboard.html` | Plotly 单文件离线 HTML，10 个联动组件 |
| 清洗后数据 | `data/clean/` | 星型模型 5 表 + SQLite 数据库 |
| 数据字典 | `docs/数据字典与星型模型.md` | 字段、类型、主外键、派生口径 |
| 合规声明 | `docs/数据来源合规声明.md` | 来源 URL、获取日期、License |

---

## 2. 目录结构

```
商业数据分析work/
├── data/
│   ├── raw/                  # 原始数据（不修改）
│   │   └── sample_-_superstore.xls
│   └── clean/                # 清洗后星型模型
│       ├── fact_sales.csv            # 10,194 × 38  订单明细事实表
│       ├── dim_customer.csv          # 804 × 15     客户维
│       ├── dim_product.csv           # 1,862 × 10   商品维
│       ├── dim_region.csv            # 4 × 2        大区维
│       ├── dim_returns.csv           # 296 × 2      退货维
│       └── superstore.db             # 上述 5 表的 SQLite 版本
├── notebooks/
│   ├── 01_数据获取与清洗.ipynb        # 读取 / 校验 / 清洗 / 派生 / 入库
│   ├── 02_商业分析模型.ipynb          # M1–M9 九类模型
│   ├── 03_可视化模板复现.ipynb        # EDA + 16 种模板（fig01–fig14、fig25、fig26）
│   └── 04_交互式大屏.ipynb            # Plotly 深色驾驶舱
├── outputs/
│   ├── figures/              # fig01–fig27
│   ├── tables/               # t01_* / t02_*
│   └── dashboard/
├── docs/                     # 论文、合规声明、数据字典
├── build/                    # 论文与 notebook 的生成脚本（可复现，非交付主体）
├── run_all.py                # 一键执行全部 notebook
├── requirements.txt
└── README.md
```

---

## 3. 环境与依赖

- Python **3.9.13**（Anaconda 发行版）
- 关键库：pandas 1.4.4 / numpy 1.21 / matplotlib 3.5.2 / seaborn 0.11.2 / plotly 5.9.0 /
  statsmodels 0.13.2 / scikit-learn 1.0.2 / scipy 1.9.1 / openpyxl 3.0.10 / xlrd 2.0.1
- 生成论文另需 python-docx 1.2.0、nbformat 5.5.0、nbclient 0.5.13
- 中文字体：微软雅黑（Windows 自带），图表内 `plt.rcParams['font.sans-serif']` 已配置

```bash
pip install -r requirements.txt
```

> 说明：项目**未使用** pyecharts / mlxtend / snownlp 等需要额外联网安装的库。
> 交互大屏改用 Anaconda 预装的 Plotly 实现（可内联 JS，离线可用）；
> Apriori 关联规则按教材定义手写实现，不依赖 mlxtend。

---

## 4. 快速开始

### 4.1 一键复现全部结果

```bash
python run_all.py
```

按 01 → 02 → 03 → 04 顺序执行，输出原地写回 notebook 并覆盖 `outputs/` 下的图表与表。
单个 notebook 约 1–3 分钟，全流程 5 分钟内完成。

```bash
python run_all.py --only 02          # 只跑第 2 个 notebook
 ```

### 4.2 在 Jupyter 里手动运行

打开 `notebooks/` 下任意 notebook，内核选择 `python3`，从上到下 Run All 即可。
notebook 内部通过向上遍历父目录自动定位项目根（`data/` 所在目录），因此**不要求**从固定路径启动。

### 4.3 打开交互大屏

直接双击 `outputs/dashboard/superstore_dashboard.html`（浏览器打开，无需服务器、无需联网）。
顶部「销售大区」下拉框驱动全部 10 个视觉元素联动。

---

## 5. 数据说明

| 项 | 内容 |
|---|---|
| 数据集 | Tableau Sample - Superstore（`sample_-_superstore.xls`） |
| 来源 | Tableau 官方示例数据页 <https://www.tableau.com/zh-cn/products/sample-data> |
| 获取方式 | 官方文件直接下载（白名单方式），未使用爬虫 |
| 规模 | 10,194 条明细 / 5,111 个订单 / 804 位客户 / 1,862 个商品 |
| 时间跨度 | 2023-01-03 ～ 2026-12-30（48 个完整月份） |
| 工作表 | `Orders`(事实) / `People`(大区经理) / `Returns`(退货清单 296 行) |
| 使用范围 | 仅用于课程作业与研究演示，遵循 Tableau 官方示例数据的使用条款 |

合规细节见 `docs/数据来源合规声明.md`。

---

## 6. 分析框架（9 类模型）

| # | 模型 | 回答的问题 | 关键参数 / 阈值依据 |
|---|---|---|---|
| M1 | 趋势与同比对比 | 增长来自哪里、是否健康 | 3 期移动平均 + 同比；谷值/峰值定位 |
| M2 | ABC / 帕累托 | 多少子类支撑了 80% 生意 | A≤70%、B 70–90%、C>90%（经典 ABC 分界） |
| M3 | 波士顿矩阵 | 各子类该投、该守还是该退 | 增长线取 2026 年整体增速 10%，份额线取相对份额 1.0 |
| M4 | RFM 八分类 | 客户价值如何分层 | R/F/M 按中位数二分 → 8 类，避免固定阈值失真 |
| M5 | K-Means 聚类 | 分层是否稳健、画像如何描述 | k=4（肘部法 + 轮廓系数 0.259），标准化后聚类，seed=42 |
| M6 | 同期群留存 | 留存是否衰减、何时该唤醒 | 只保留样本 ≥20 人的 2023 年 12 个 cohort，加权平均 |
| M7 | Apriori 关联规则 | 哪些商品该捆绑 | support≥1%、confidence≥15%、lift>1.05（按数据分布下调后得 11 条） |
| M8 | 履约健康度漏斗 | 订单在哪一环流失 | 下单 → 履约≤4 天 → 未退货 → 盈利，四层订单级漏斗 |
| M9 | SARIMA 时间序列 | 未来 6 个月 GMV 区间 | 网格搜索 4 组 (p,d,q)(P,D,Q,12)，AIC 选 (0,1,1)(0,1,1,12) |

模型评估：SARIMA 留出法回测 **MAPE 18.38% / RMSE 17,877 美元**；K-Means 轮廓系数 0.2591，与 RFM 分层结论方向一致（交叉验证）。

---

## 7. 关键结论（均有数据支撑）

1. **增长在量不在价**：4 年 GMV 232.65 万美元、2026 年同比 +21.44%，但客单价从 2023 年的 496.52 美元降至 2026 年的 432.71 美元，增长由订单频次驱动。
2. **折扣是第一利润漏损**：整体利润率 12.56%，折扣 ≥20% 后平均利润率转负，≥40% 时长期处于 −36%～−180%；建议折扣红线设在 20%。
3. **结构错位**：Office Supplies 占 60.1% 明细行仅贡献 31.5% 销售额；Technology 以 36.1% 销售额贡献 17.4% 利润率；Furniture 销售额 32.4% 但利润率仅 2.6%（Tables −8.53%）。
4. **客户高度集中且正在沉默**：25.4% 的重要价值客户贡献 40.2% 销售额；14.4% 的高价值客户已沉默 174 天以上，对应 116 人召回名单。
5. **履约是最大流失环节**：5,111 单中仅 44.6% 走到「达标·未退货·盈利」，履约环节漏损 39.8%，盈利环节再漏 21.2%。

商业建议：折扣分级审批、高价值客户召回、办公三件套（Binders + Paper + Storage）捆绑、区域差异化促销（Central 利润率仅 7.92%）、季度滚动预测。

---

## 8. 复现约定

- **随机种子固定为 42**（`RANDOM_SEED = 42`），贯穿抽样、K-Means、SARIMA 网格搜索。
- **全量不抽样**：所有模型使用全部 10,194 行明细；仅散点图（fig10）为可视清晰抽样 4,000 行，并在图题中注明。
- **金额口径**：`Sales` 为折后销售额，`Profit` 为利润，`Profit Margin = Profit / Sales`；利润率均为加权口径（Σ利润/Σ销售额），不是行级利润率的算术平均。
- **图号与文件名一一对应**，图号 1–27 与正文出现顺序严格一致，附录 C 给出完整索引表。
- 清洗过程保留 `is_sales_outlier` / `is_profit_outlier` 标记列，**只标记不删除**，避免人为裁剪真实业务的长尾。

---

## 9. 学术诚信与 AI 使用披露

- 数据来源合规、可追溯，未使用任何非白名单渠道（无爬虫、无破解、无二次转售数据）。
- 全部图表均由 Python 代码生成，**未使用 Power BI / Tableau / Fine BI 截图，也未使用 Excel 图表截图**。
- AI 工具在代码结构梳理、图表样式调试、论文文字润色环节提供了辅助；所有模型参数、阈值、结论均以本仓库代码的实际运行输出为准，
  并经过人工复核（详见论文 7.3 节「AI 使用披露」）。

---

## 10. 提交前需替换的占位信息

论文封面与附录 B 中以下四项为占位内容，请替换为本人信息后再提交：

| 位置 | 占位值 | 替换为 |
|---|---|---|
| 封面 | 姓名 `肖某某` | 本人姓名 |
| 封面 | 学号 `2023XXXXXX` | 本人学号 |
| 封面 | 班级 `数据科学与大数据技术 23XX 班` | 本人班级 |
| 附录 B | `https://gitee.com/xxx/superstore-analysis` | 实际仓库地址 |
| 封面 | 完成日期 `2026 年 11 月 3 日` | 实际提交日期 |

修改方式：编辑 `build/paper_base.py` 顶部的 `AUTHOR / STUDENT_ID / CLASS_NAME / COLLEGE / FINISH_DATE` 与
`build/paper_content.py` 附录 B 的仓库地址，然后执行：

```bash
python build/build_paper.py     # 重新生成 docx
python build/export_pdf.py      # 可选：导出 PDF 预览
```
