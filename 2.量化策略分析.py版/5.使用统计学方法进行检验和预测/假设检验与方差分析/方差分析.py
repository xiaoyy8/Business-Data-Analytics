# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：方差分析.ipynb

# ----------------------------------------------------------------------

# ## 单因素方差分析

# ----------------------------------------------------------------------

# %%

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pandas as pd

# %%

data = pd.read_csv('creditcard_exp.csv')
df = data[['avg_exp','edu_class','gender']].dropna(how='any',axis=0)
df['edu_class'] = df['edu_class'].astype('str')
df['gender'] = df['gender'].astype('str')

# %%

df['avg_exp'] = df['avg_exp'].apply(lambda x: 0 if x==' ' else x)
df['avg_exp'] = df['avg_exp'].astype('float')

# %%

formula = f'avg_exp ~ C(edu_class) + C(gender)'
anova = ols(formula=formula, data=df).fit()
anova_results = anova.summary()
print(anova_results)

# ----------------------------------------------------------------------

# ## 多因素方差分析

# ----------------------------------------------------------------------

# %%

data = pd.read_csv('creditcard_exp.csv')
df = data[['avg_exp','edu_class','gender']].dropna(how='any',axis=0)
df['edu_class'] = df['edu_class'].astype('str')
df['gender'] = df['gender'].astype('str')
df['avg_exp'] = df['avg_exp'].apply(lambda x: 0 if x==' ' else x)
df['avg_exp'] = df['avg_exp'].astype('float')

# %%

formula = f'avg_exp ~ C(edu_class) + C(gender) + C(edu_class)*C(gender)'

anova = ols(formula=formula, data=df).fit()
anova_results = anova.summary()
print(anova_results)
