# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：5.社交网络算法-小案例.ipynb

# ----------------------------------------------------------------------

# ### 社交网络分析

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------

# #### 社交网络算法-小案例

#

# 导入相关的包

# ----------------------------------------------------------------------

# %%

import networkx as nx  
import pandas as pd
import matplotlib.pyplot as plt

# %%

#nx.test()

# %%

edge_list=pd.read_csv('./data/stormofswords.csv')
edge_list.head()

# %%

edge_list.Weight=edge_list.Weight.astype(int)

# %%

#edge_list

# %%

def plot_network(pd_table):
    '''
    绘制网络关系图
    '''
    G = nx.from_pandas_edgelist(edge_list, source = 'Source', target = 'Target', 
                                edge_attr = 'Weight',create_using = nx.DiGraph())
    nx.draw(G,
        #pos = nx.spiral_layout(G),
        node_color = 'b', 
        edge_color = 'r',
        with_labels = True,
        font_size =10,
        node_size =20)
    plt.show()

# %%

plot_network(edge_list)
