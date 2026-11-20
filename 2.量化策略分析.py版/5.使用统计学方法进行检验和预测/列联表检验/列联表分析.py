# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：列联表分析.ipynb

# %%

import pandas as pd
accepts =pd.read_csv ( 'accepts.csv' )
cross_table=pd.crosstab(accepts.bankruptcy_ind,accepts.bad_ind, margins=True)
cross_table

# %%

cross_table_rowpct = cross_table.div(cross_table ["All"] ,axis = 0)
cross_table_rowpct

# %%

# 打印结果
from scipy import stats
print(
    "chisq = %6.4f\np-value = %6.4f\ndof = %d\nexpected_freq = %s"
    %stats.chi2_contingency (cross_table))
