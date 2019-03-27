# -*- coding: UTF-8 -*-
'''
@ Author: Kasper
Created on Wednesday, March 27, 2019
Contrarian Strategy Analysis
'''
import os; path = os.getcwd()
import pandas as pd

# 股票数量研究。

# 股票数量对小市值策略的影响。
total_data = pd.DataFrame()
for limit in range(0, 501, 10):
    file_name = " ".join(["Loser", str(limit), "0901-1901"])
    data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % file_name)
    total_data = total_data.join(data)

data1 = pd.read_csv(path + "\\Contrarian Result\\Loser 0 0901-1901.csv" % file_name)