# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：1.主成分_因子分析_层次聚类(经济发展数据).ipynb

# ----------------------------------------------------------------------

# ### cities_10记录了十个沿海省份的经济指标，通过降维方法对各省、市经济发展情况

#

# 变量含义如下：

#

# |变量|含义|

# |:--:|:--:|

# |AREA|地区|

# |X1|GDP|

# |X2|人均GDP|

# |X3|工业增加值|

# |X4|第三产业增加值|

# |X5|固定资产投资|

# |X6|基本建设投资|

# |X7|社会消费品零售总额|

# |X8|海关出口总额|

# |X9|地方财政收入|

# ----------------------------------------------------------------------

# %%

# %matplotlib inline

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pd.set_option('display.max_columns', 8)

# %%

cities = pd.read_csv("cities_10.csv", encoding='gbk')
cities.head()

# %%

cities.loc[:, 'X1':].corr(method='pearson').head()

# ----------------------------------------------------------------------

# ### 主成分分析（预先进行标准化）

# - [数据标准化参考](http://www.cnblogs.com/chaosimple/p/4153167.html)

# ----------------------------------------------------------------------

# %%

from sklearn.preprocessing import StandardScaler

n_components = 2

scaler = StandardScaler()
scale_cities = scaler.fit_transform(cities.loc[:, 'X1':])

pca = PCA(n_components=n_components)
pca_scores = pca.fit_transform(scale_cities)
print('Cumsum of explained variance ratio: ', 
      pca.explained_variance_ratio_.cumsum())

# %%

pca_scores = pd.DataFrame(pca_scores, columns=['Gross', 'Avg'])
scale_pca_cities = cities.join(pca_scores)
scale_pca_cities.head()

# %%

# 主成分的业务解释
print(pca.components_)

# %%

from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题

def scatter(x, y, labels, **kw):
    plt.figure(figsize=(6, 4))
    plt.yticks(size=12)
    plt.xticks(size=12)
    plt.scatter(x, y)
    for xx, yy, label in zip(x, y, labels):
        plt.text(xx, yy, '%s.' % label, 
                 ha='center', va='bottom', **kw)
    plt.show()

x = scale_pca_cities['Gross']
y = scale_pca_cities['Avg']
labels = scale_pca_cities['AREA']
scatter(x, y, labels, fontsize=15)

# ----------------------------------------------------------------------

# ### *稀疏主成分分析 SparsePCA

#

# [SparsePCA文档说明](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.SparsePCA.html#sklearn.decomposition.SparsePCA)

# ----------------------------------------------------------------------

# %%

from sklearn.decomposition import SparsePCA
alpha = 0.5
spca = SparsePCA(n_components=n_components, alpha=alpha)
spca.fit(scale_cities)
pd.DataFrame(spca.components_)

# ----------------------------------------------------------------------

# 选择合适的稀疏度

# ----------------------------------------------------------------------

# %%

from functools import reduce

n_cols = scale_cities.shape[1]
spca_with_alpha = []

for i in np.arange(0.1, 1, 0.05):
    spca = SparsePCA(n_components=n_components, alpha=i)
    spca.fit(scale_cities)
    components_ = pd.DataFrame(spca.components_).T
    diff = np.count_nonzero(components_) - n_cols
    spca_with_alpha.append((i, diff))

selector = pd.DataFrame(spca_with_alpha)
selector.T

# %%

spca_ = SparsePCA(n_components=n_components, alpha=0.65).fit(scale_cities)
pd.DataFrame(spca_.components_)

# %%

scale_spca_cities = pd.DataFrame(spca_.transform(scale_cities), columns=['Gross', 'Avg'])
scale_spca_cities

# %%

x = scale_spca_cities['Gross']
y = scale_spca_cities['Avg']
label = cities['AREA']

scatter(x, y, label)

# ----------------------------------------------------------------------

# ### 因子分析

#

# pip install fa_kit first！

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# - 使用fa_kit包，参考https://github.com/bmcmenamin/fa_kit

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# - 1、导入包，并对输入的数据进行主成分提取。

# ----------------------------------------------------------------------

# %%

from fa_kit import FactorAnalysis
from fa_kit import plotting as fa_plotting

fa = FactorAnalysis.load_data_samples(
        scale_cities,
        preproc_demean=True,
        preproc_scale=True
        )
fa.extract_components()

# ----------------------------------------------------------------------

# - 2、设定提取主成分的方式。默认为“broken_stick”方法，建议使用“top_n”法

# ----------------------------------------------------------------------

# %%

fa.find_comps_to_retain(method='top_n',num_keep=2)

# ----------------------------------------------------------------------

# - 3、通过最大方差法进行因子旋转

# ----------------------------------------------------------------------

# %%

from pylab import mpl

mpl.rcParams['axes.titlesize'] = 20    #  指定title大小
mpl.rcParams['xtick.labelsize'] = 15   #  指定x刻度大小
mpl.rcParams['ytick.labelsize'] = 15   #  指定y刻度大小

fa.rotate_components(method='varimax') #  最大方差因子旋转
fa_plotting.graph_summary(fa)          #  绘制因子载荷矩阵与原始变量的关系

plt.show()

# ----------------------------------------------------------------------

# - 4、获取因子得分

# ----------------------------------------------------------------------

# %%

print(fa.comps['rot'])

# %%

fa_scores = fa.get_component_scores(scale_cities)  # 因子得分
# Equals to ```np.dot(scale_cities, fa_comps)```

cities_factor_analysis = cities.join(
    pd.DataFrame(fa_scores, columns=['Gross', 'Avg']))
cities_factor_analysis.to_csv('cities_FA_score.csv', index=False)
cities_factor_analysis.head()

# %%

x = cities_factor_analysis['Gross']
y = cities_factor_analysis['Avg']
label = cities_factor_analysis['AREA']

scatter(x, y, label,fontsize=15)

# ----------------------------------------------------------------------

# ### 层次聚类

# ----------------------------------------------------------------------

# %%

import scipy.cluster.hierarchy as sch

#  生成点与点之间的欧式距离矩阵
distMat = sch.distance.pdist(
    cities_factor_analysis[['Gross','Avg']],'euclidean') 

#  ward法进行层次聚类
Z = sch.linkage(distMat, method='ward') 

#  生成聚类树状图
fig, ax = plt.subplots(figsize=(6, 4)) 
P = sch.dendrogram(
    Z,                                               
    ax=ax,                                           # 设置绘制的轴
    labels=cities_factor_analysis['AREA'].tolist(),  # 设置标签
    leaf_font_size=15,                               # 设置标签字体大小
    leaf_rotation=90                                 # 设置标签字体方向
)  

plt.savefig('plot_dendrogram1.png')
plt.show()

# %%

labels = sch.cut_tree(Z, n_clusters=2)
cities_factor_analysis['cluster'] = labels

#  获取每个簇的中心
cities_factor_analysis.loc[:, 'X1':'X9'].groupby(
    cities_factor_analysis['cluster']).mean().T
