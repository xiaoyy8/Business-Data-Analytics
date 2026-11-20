# -*- coding: utf-8 -*-
# 由 Jupyter Notebook 自动转换生成：3.二次规划.ipynb

# ----------------------------------------------------------------------

# ### 二次规划

# ----------------------------------------------------------------------

# %%

import cplex

op = cplex.Cplex()
op.read("qp1.lp")
op.solve()
# 输出结果
print(op.solution.get_objective_value())
print(op.solution.get_values())
