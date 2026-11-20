# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：旭日图_jupyter.ipynb

# ----------------------------------------------------------------------

# # 嘉兴大学本科专业设置（两层交互式旭日图）

#

# **数据源**：嘉兴大学普通高等学校本科专业设置一览表.xlsx

#

# **层级**：第 1 层 学院 → 第 2 层 专业，扇区面积 = 该学院的专业数

#

# **交互**：悬停看详情 ； 点击内圈学院放大 ； 点击圆心返回全貌 ； 右上角相机可存图

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# ## 0. 安装依赖

# ----------------------------------------------------------------------

# %%

# %pip install -q pandas openpyxl plotly -i https://pypi.tuna.tsinghua.edu.cn/simple

# %%

import pandas
import openpyxl
import plotly

print(f"pandas 安装路径: {pandas.__file__}")
print(f"openpyxl 安装路径: {openpyxl.__file__}")
print(f"plotly 安装路径: {plotly.__file__}")

# %%

import site
print(site.getsitepackages())

# ----------------------------------------------------------------------

# ## 1. 参数配置

# ----------------------------------------------------------------------

# %%

import os
import re

import pandas as pd
import plotly.express as px
import plotly.io as pio

XLSX_PATH = r"嘉兴大学普通高等学校本科专业设置一览表.xlsx"

SHEET_NAME  = 0           
COL_COLLEGE = "学院"      
COL_MAJOR   = "专业名称"   

SHORT_LABEL = True        
DARK        = False       
PALETTE     = px.colors.qualitative.Alphabet   

assert os.path.exists(XLSX_PATH), f"路径不存在：{XLSX_PATH}"

# ----------------------------------------------------------------------

# ## 2. 读取与清洗

# ----------------------------------------------------------------------

# %%

df = pd.read_excel(XLSX_PATH, sheet_name=SHEET_NAME, usecols=[COL_COLLEGE, COL_MAJOR])

df[COL_COLLEGE] = df[COL_COLLEGE].ffill()
df[COL_MAJOR]   = df[COL_MAJOR].ffill()      

for c in (COL_COLLEGE, COL_MAJOR):
    df[c] = df[c].astype("string").str.strip()

df = df.dropna(subset=[COL_COLLEGE, COL_MAJOR])
df = df[(df[COL_COLLEGE] != "") & (df[COL_MAJOR] != "")]
df = df[df[COL_MAJOR] != COL_MAJOR]                       
df = df.drop_duplicates(subset=[COL_COLLEGE, COL_MAJOR])   
df = df.reset_index(drop=True)

print(f"共 {df[COL_COLLEGE].nunique()} 个学院、{len(df)} 个专业")
df.head()

# ----------------------------------------------------------------------

# ### 2.1各学院专业数（降序）

# ----------------------------------------------------------------------

# %%

cnt = df[COL_COLLEGE].value_counts()
cnt.to_frame("专业数")

# ----------------------------------------------------------------------

# ## 3. 绘制两层旭日图

# ----------------------------------------------------------------------

# %%

def short_name(name):
    if not SHORT_LABEL:
        return name
    s = re.sub(r"[（(][^）)]*[）)]", "", name).strip()
    return s or name

d = df.copy()
d["专业数"] = 1                                   

cnt_map = d.groupby(COL_COLLEGE, sort=False)[COL_MAJOR].size()
d["学院_标注"] = d[COL_COLLEGE].map(lambda x: f"{short_name(x)}  ({cnt_map[x]})")

order = list(dict.fromkeys(d[COL_COLLEGE]))
color_map = {f"{short_name(c)}  ({cnt_map[c]})": PALETTE[i % len(PALETTE)]
             for i, c in enumerate(order)}

fig = px.sunburst(
    d,
    path=["学院_标注", COL_MAJOR],
    values="专业数",
    color="学院_标注",
    color_discrete_map=color_map,
    branchvalues="total",
)

fig.update_traces(
    textinfo="label",
    insidetextorientation="radial",
    rotation=90,                                    
    marker=dict(line=dict(color="rgba(255,255,255,0.6)", width=1)),
    hovertemplate=(
        "<b>%{label}</b><br>"
        "所属学院：%{parent}<br>"
        "专业数：%{value}<br>"
        "占本院比例：%{percentParent:.1%}"
        "<extra></extra>"
    ),
)

paper, font_color = ("#111318", "#E9ECF1") if DARK else ("#FFFFFF", "#1F2328")

fig.update_layout(
    title=dict(
        text=("<b>嘉兴大学本科专业设置</b><br>"
              f"<sup>{len(order)} 个学院 · {len(d)} 个本科专业　|　"
              "点击内圈放大，点击圆心返回</sup>"),
        x=0.5, xanchor="center", font=dict(size=22, color=font_color),
    ),
    paper_bgcolor=paper,
    plot_bgcolor=paper,
    font=dict(family="Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif",
              size=12, color=font_color),
    margin=dict(t=100, l=10, r=10, b=10),
    width=820, height=820,
)

fig.show()

# ----------------------------------------------------------------------

# ## 4. 分析

#

# **内圈**：15 个学院，扇形角度/面积 = 该学院的专业数，括号里是专业数

#

# **外圈**：63 个专业，颜色跟随所属学院，同一个学院的专业是同一色系

#

# **注意**：商学院 7 个专业最"宽"；马克思主义学院（中共党史党建学院）只有 1 个专业，扇区最窄；工科类（机械、信息、人工智能、建工、材纺、生化）合计占比接近一半，符合应用型大学的学科结构

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# ## 5. 导出文件

# ----------------------------------------------------------------------

# %%

fig.write_html("嘉兴大学本科专业_旭日图.html", include_plotlyjs=True)
print("已导出")
