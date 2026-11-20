# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：描述性统计分析与绘图.ipynb

# ----------------------------------------------------------------------

# ## 连续变量的分布与集中趋势

# ----------------------------------------------------------------------

# %%

import pandas as pd
data = pd.read_csv('sndHsPr.csv')

# %%

data.price.agg(['mean','median','std'])

# %%

data. price.quantile([0.25,0.5,0.75])

# %%

data.price.hist(bins=20)

# ----------------------------------------------------------------------

# ## 连续变量的离散程度

# ----------------------------------------------------------------------

# %%

data.price.max()-data.price.min()

# %%

data.price.var()#求方差

# %%

data.price.std()#求标准差

# ----------------------------------------------------------------------

# ## 数据分布的对称与高矮

# ----------------------------------------------------------------------

# %%

import numpy as np

# %%

normal = pd.Series(np.random.randn(1000),name='normal')

# %%

normal.skew()

# %%

normal.kurtosis()

# %%

data[['AREA','price']].corr("pearson")

# %%

data[['AREA','price']].corr("spearman")

# %%

data[['AREA','price']].corr("kendall")
