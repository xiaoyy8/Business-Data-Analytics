# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：数据预处理.ipynb

# %%

import pandas as pd
import os
import numpy as np
# 导入数据
camp = pd.read_csv(r"teleco_camp_orig.csv")
# 脏数据或数据不正确
import matplotlib.pyplot as plt
plt.hist(camp["AvgIncome"],bins=20)#,normed=True)#查看分布情况

# %%

camp["AvgIncome"].describe(include="all")

# %%

camp["AvgHomeValue"].describe(include="all")

# %%

#这里的 0值应该是缺失值，处理 0值。
camp["AvgIncome"]=camp["AvgIncome"].replace({0:np.NaN})

# %%

#像这种外部获取的数据要比较小心，经常出现意义不清晰或这错误值。AvgHomeValue也有这种情况
plt.hist(camp["AvgIncome"],bins=20,range=(camp.AvgIncome.min(),camp.AvgIncome.max()))
#由于数据中存在缺失值 ,需要指定绘图的值域

# %%

camp["AvgHomeValue"].describe(include="all")
