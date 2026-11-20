# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：序列模式（银行产品交叉销售分析）.ipynb

# ----------------------------------------------------------------------

# ### AprioriAll

# ----------------------------------------------------------------------

# %%

import pandas as pd

data = pd.read_csv('bank_prod_order.csv', encoding='gbk')

# 按照订单编号与用户编号分组汇总
baskets = data.groupby(['OrderNumber', 'CSR_ID'])['PROD'].apply(list)
baskets.head()

# %%

# 按照用户编号分组汇总
baskets = baskets.groupby(level=1).apply(list)
baskets.head()

# %%

import sys
sys.path.append('./myscript')  # aprioriAll.py放在'./myscript'文件夹下
from aprioriAll import aprioriAll

patterns = aprioriAll(baskets, min_support=0.1)
patterns.head()

# ----------------------------------------------------------------------

# ### prefixspan算法

# ----------------------------------------------------------------------

# %%

import sys

sys.path.append('./myscript')  # prefixspan.py放在'./myscript'下

from prefixspan import SquencePattern, prefixSpan

patterns = prefixSpan(SquencePattern([], 1e4), baskets, threshold=100)
for pattern in patterns:
    print(pattern.squence, "-> support:", pattern.support)
