# -*- coding: UTF-8 -*-
'''
@ Author: Kasper
Created on Wednesday, March 27, 2019
Contrarian Strategy Analysis
'''
import os; path = os.getcwd()
import pandas as pd

# 股票数量研究。

# 股票数量对小市值的影响。
small_market_capital_with_different_limit = pd.DataFrame()
for limit in range(0, 501, 10)