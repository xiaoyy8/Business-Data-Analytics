# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：主成分分析.ipynb

# ----------------------------------------------------------------------

# ## 在 Python 中实现主成分分析. 

# 一家电信运营商希望根据客户在几个主要业务上的使用情况，对客户进行分群

# 分析。

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# ![image.png](attachment:image.png)

# ----------------------------------------------------------------------

# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%

profile = pd.read_csv("profile_telecom.csv")
profile.head()

# %%

data = profile.loc[:,"cnt_call":]
data.corr(method = "pearson")

# %%

from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
data_scaled = scale(data)
pca = PCA(n_components = 2, whiten = True).fit(data_scaled)
pca.explained_variance_ratio_

# %%

pca.components_

# %%

pca.transform(data_scaled)
