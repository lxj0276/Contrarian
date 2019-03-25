# -*- coding: UTF-8 -*-
'''
@ Author: Kasper
Created on Sunday, March 24, 2019
Contrarian Strategy Backtest
'''

#%%
import os
path = os.getcwd()
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from functools import partial
from Contrarian import get_strategy_monthly_return
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import ffn

#%%
def backtest(
    start, 
    end, 
    strategy_name, 
    equity=True, 
    benchmark=True, 
    excess_return=True, 
    transaction_cost=True, 
    equity_plot=True, 
    profit_plot=True
):

    if not os.path.isfile(path + "\\Contrarian Result\\%s.csv" % strategy_name):
        start_date = dt.strptime(start, '%Y-%m')
        end_date = dt.strptime(end, '%Y-%m')
        time_span = relativedelta(end_date, start_date).years*12 + relativedelta(end_date, start_date).months

        backtest_data = pd.DataFrame()
        for date in [(dt.strptime(start, '%Y-%m') + relativedelta(months=i)).strftime('%Y-%m') for i in range(time_span)]:
            print(date, ":")
            next_df = strategy(start_time=date)
            backtest_data = pd.concat(
                [backtest_data, next_df], 
                axis=0
            )
            
        if benchmark:
            hs300 = pd.read_csv(path+"\\Contrarian Data\\benchmark\\benchmark.csv")
            hs300 = hs300[["Month", "Idxrtn"]]
            hs300.columns = ["Month", "Benchmark Profit"]
            hs300.index = pd.to_datetime(hs300["Month"], format='%Y-%m')
            hs300 = hs300[["Benchmark Profit"]]
            backtest_data = backtest_data.join(hs300)
        
        if excess_return:
            backtest_data["Excess Return"] = backtest_data["Profit"] - backtest_data["Benchmark Profit"]

        if transaction_cost:
            backtest_data["Equity"] = ((backtest_data["Profit"]+1) * 0.998**2).cumprod() * 100
            if "Benchmark Profit" in backtest_data.columns:
                backtest_data["Benchmark Equity"] = ((backtest_data["Benchmark Profit"]+1) * 0.998**2).cumprod() * 100
        else:
            backtest_data["Equity"] = (backtest_data["Profit"]+1).cumprod() * 100
            if "Benchmark Profit" in backtest_data.columns:
                backtest_data["Benchmark Equity"] = (backtest_data["Benchmark Profit"]+1).cumprod() * 100

        print("回测完成，数据已保存至本地。")
        backtest_data.to_csv(path + "\\Contrarian Result\\%s.csv" % strategy_name)
    
    else:
        backtest_data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % strategy_name, index_col=[0])
    
    CAGR = round(((backtest_data["Equity"].iloc[-1]/100)**(1/10) - 1) * 100, 3)
    print("策略年化复合增长率为%s" % CAGR + "%。")

    if equity_plot:
        # plt.figure(figsize=(8, 5))
        pass
    if profit_plot:
        pass

    return backtest_data

strategy = partial(
    get_strategy_monthly_return, 
    loser=True, 
    winner=False, 
    small=True, 
    large=False, 
    rank_time=3, 
    hold_time=1, 
    limit=100, 
    priority="market_capital", 
    multiplier=2, 
    ST=False
)

backtest_data = backtest(
    start="2018-01", 
    end="2019-01", 
    strategy_name="Loser Small 3-1 100 market_capital 2 no_ST 1801-1901"
)

#%%
plt.figure(figsize=(8, 5))
plt.plot(x = backtest_data.index, y = backtest_data["Equity"])
plt.savefig(path + "\\Contrarian Result\\test.png")