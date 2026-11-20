# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：关联规则（银行产品交叉销售分析）.ipynb

# ----------------------------------------------------------------------

# ### Apriori

# ----------------------------------------------------------------------

# %%

import pandas as pd

data = pd.read_csv('bank_prod_order.csv',encoding='gbk')
data.head()

# %%

baskets = data['PROD'].groupby(data['CSR_ID']).apply(list)
baskets.head()

# %%

import sys
sys.path.append('./myscript')
from apriori import arules

rules = arules(baskets, min_support=0.02)
rules.head()

# ----------------------------------------------------------------------

# 可以根据需要进行后续处理，例如按照confidence和lift过滤后，按support排序

# ----------------------------------------------------------------------

# %%

conf = rules[(rules.confidence > 0.1) & (rules.lift > 1)]
conf.sort_values(by='support', ascending=False).head()

# ----------------------------------------------------------------------

# 如果有必要，我们也可以通过图形看一下规则在支持度、置信度和提升度上的分布情况

# ----------------------------------------------------------------------

# %%

import matplotlib.pyplot as plt
# %matplotlib inline

ax = plt.subplot()
ax.set_xlabel('lift')
conf.plot.scatter(x="lift", y="support",c="confidence",cmap='binary',
                  figsize=(6,4), ax=ax)

plt.show()

# ----------------------------------------------------------------------

# ### FP_growth

#

# `pip install Orange3-Associate` first!

#

# [参考文档](https://orange3-associate.readthedocs.io/en/latest/scripting.html)

# ----------------------------------------------------------------------

# %%

mapping = data['PROD'].drop_duplicates().to_dict()  # 生成{编号:产品}映射
inverse_mapping = {v:k for k, v in mapping.items()}     # 生成{产品:编号}映射

data['PROD'] = data['PROD'].replace(inverse_mapping)  # 将产品用编号替代
baskets = data['PROD'].groupby(data['CSR_ID']).apply(list)  
baskets.head()

# %%

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

# 1. 数据格式转换
te = TransactionEncoder()
te_ary = te.fit(baskets).transform(baskets)
df = pd.DataFrame(te_ary, columns=te.columns_)

# 2. 运行 FP-Growth
frequent_itemsets = fpgrowth(df, min_support=0.02, use_colnames=True)

# 3. 生成关联规则
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

# 4. 整理结果，并还原产品名称
rules = rules.rename(columns={'antecedents': 'atecedent', 'consequents': 'consequent'})
pid_to_product = lambda fsets: tuple(mapping[int(fset)] for fset in fsets)
rules['atecedent'] = rules['atecedent'].apply(pid_to_product)
rules['consequent'] = rules['consequent'].apply(pid_to_product)

rules.head()

# ----------------------------------------------------------------------

# - atecedent (frozenset) – The LHS of the association rule.

# - consequent (frozenset) – The RHS of the association rule.

# - support (int) – Support as an absolute number of instances.

# - confidence (float) – The confidence percent, calculated as: total_support / lhs_rupport.

# - coverage (float) – Calculated as: lhs_support / n_examples

# - strength (float) – Calculated as: rhs_support / lhs_examples

# - lift (float) – Calculated as: n_examples * total_support / lhs_support / rhs_support

# - leverage (float) – Calculated as: (total_support * n_examples - lhs_support * rhs_support) / n_examples**2

# ----------------------------------------------------------------------
