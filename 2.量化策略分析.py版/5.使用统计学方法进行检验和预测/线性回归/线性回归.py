# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：线性回归.ipynb

# %%

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# ----------------------------------------------------------------------

# ## 读取变量

# ----------------------------------------------------------------------

# %%

import numpy as np
import pandas as pd

# %%

#读取数据
data_raw = pd.read_excel('LR_practice.xlsx')
data_raw.head()

# %%

data_raw.tail()

# %%

data_raw.head(2)

# %%

#数据基本信息
data_raw.info()

# ----------------------------------------------------------------------

# ## 数据清洗

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# ### 删除无用变量

# ----------------------------------------------------------------------

# %%

#变量'id','Acc','edad2'
data_raw.drop(['id','Acc','edad2'], axis=1, inplace=True)

# %%

data_raw.head(2)

# ----------------------------------------------------------------------

# ### 重复值

# ----------------------------------------------------------------------

# %%

#删除重复值
data_raw.drop_duplicates(inplace=True)

# ----------------------------------------------------------------------

# ### 缺失值

# ----------------------------------------------------------------------

# %%

#查看缺失情况
data_raw.isnull().mean()

# %%

data_raw.isnull().sum()

# ----------------------------------------------------------------------

# #### 填补缺失值

# ----------------------------------------------------------------------

# %%

data_raw['avg_exp'].mean()

# %%

#avg_exp
data_raw['avg_exp'] = data_raw['avg_exp'].fillna(data_raw['avg_exp'].mean())

# %%

data_raw.isnull().mean()

# ----------------------------------------------------------------------

# #### 数据编码和缺失值

# ----------------------------------------------------------------------

# %%

#方法1：gender
data_raw['gender'] = data_raw['gender'].map({'Male':1, 'Female':0})

# %%

data_raw.head(2)

# %%

#方法2：edu_class
data_raw['edu_class'].unique()

# %%

label = data_raw['edu_class'].unique().tolist()
label

# %%

label.index('中学')

# %%

#对原数据进行编码
data_raw['edu_class'] = data_raw['edu_class'].apply(lambda x: label.index(x))

# %%

data_raw.head()

# %%

data_raw['edu_class'].value_counts()

# ----------------------------------------------------------------------

# ### 异常值

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# #### 箱线图

# ----------------------------------------------------------------------

# %%

import seaborn as sns

# %%

# dist_avg_income
sns.boxplot(data=data_raw['dist_avg_income'])

# ----------------------------------------------------------------------

# #### 3倍标准差

# ----------------------------------------------------------------------

# %%

from scipy import stats

# %%

#标准化数据(Age)
z = stats.zscore(data_raw['Age'])
z

# %%

(z>3)|(z<-3)

# %%

#寻找异常数据的索引
z[(z>3)|(z<-3)]

# %%

#查看异常数据的值
data_raw['Age'].iloc[40]

# ----------------------------------------------------------------------

# 如何填补999这个异常的年龄数据呢？

# ----------------------------------------------------------------------

# %%

data_raw['Age'].mean()

# %%

data_raw['Age'].drop(index=40).mean()

# %%

#将异常值使用除异常值之外的数据的均值进行填补
# 1. 先计算出除了第40行之外的平均年龄
mean_age = data_raw['Age'].drop(index=40).mean()

# 2. 直接精准定位并填入
data_raw.loc[40, 'Age'] = mean_age

# ----------------------------------------------------------------------

# ### 哑变量转换

# ----------------------------------------------------------------------

# %%

data_raw.head()

# %%

#edu_class
dummy = pd.get_dummies(data=data_raw['edu_class'], prefix='edu', drop_first=True)
dummy

# %%

#合并到原数据
data = pd.concat([data_raw, dummy], axis=1)
data.head()

# ----------------------------------------------------------------------

# ## 相关分析

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# ### 相关系数

# ----------------------------------------------------------------------

# %%

data.corr()

# %%

#分类变量
data.corr(method='kendall')

# ----------------------------------------------------------------------

# ### 散点图

# ----------------------------------------------------------------------

# %%

import matplotlib.pyplot as plt

# %%

# avg_exp和Income
plt.scatter(data['Income'], data['avg_exp'])

# ----------------------------------------------------------------------

# ## 回归分析

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# ### 回归模型

# ----------------------------------------------------------------------

# %%

from statsmodels.formula.api import ols

# %%

data.columns

# %%

data.head()

# %%

# model_1 = ols(LR1, data)
# model_1 = model_1.fit()

# %%

LR1 = 'avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+ dist_avg_income+edu_1+ edu_2+edu_3+ edu_4'
model_1 = ols(LR1, data).fit()

# %%

model_1.summary()

# %%

#常用接口
dir(model_1)

# %%

model_1.resid

# ----------------------------------------------------------------------

# ### 模型调优

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# #### 共线性

# ----------------------------------------------------------------------

# %%

data.head()

# %%

def vif(df, y_col):
    x_cols = list(df.columns)
    x_cols.remove(y_col)
    formula = y_col + '~' + '+'.join(x_cols)
    rsquared = ols(formula, df).fit().rsquared
    return 1. / (1. - rsquared)

exog = data[['gender','Age','Income','Ownrent','Selfempl','dist_home_val','dist_avg_income','edu_class']]

for y_col in exog.columns:
    print(y_col, '\t', vif(df=exog, y_col=y_col))

# %%

#重新拟合模型
LR2 = 'avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4'
model_2 = ols(LR2, data).fit()
model_2.summary()

# ----------------------------------------------------------------------

# #### 同方差

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# 残差图：   

# - 一元回归：横坐标是X，纵坐标是残差

# - 多元回归：横坐标是Y的拟合值，纵坐标是残差

# ----------------------------------------------------------------------

# %%

#残差图
plt.scatter(model_2.predict(data), model_2.resid)

# ----------------------------------------------------------------------

# #### 正态性

# ----------------------------------------------------------------------

# %%

res = stats.probplot(model_2.resid, plot=plt)

# %%

data['ln_avg_exp'] = np.log(data['avg_exp'])
data.head()

# %%

#重新拟合模型
LR3 = 'ln_avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4'
model_3 = ols(LR3, data).fit()
model_3.summary()

# ----------------------------------------------------------------------

# ![image.png](attachment:image.png)

# ----------------------------------------------------------------------

# %%

res = stats.probplot(model_3.resid, plot=plt)

# ----------------------------------------------------------------------

# #### 高次项

# ----------------------------------------------------------------------

# %%

data['Age_sq'] = data['Age']**2
data.head()

# %%

#年龄
LR4 = 'ln_avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4 + Age_sq'
model_4 = ols(LR4, data).fit()
model_4.summary()

# ----------------------------------------------------------------------

# #### 交互项

# ----------------------------------------------------------------------

# %%

data['Age_gender'] = data['Age']*data['gender']
data.head()

# %%

LR5 = 'ln_avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4 + Age_sq+Age_gender'
model_5 = ols(LR5, data).fit()
model_5.summary()
