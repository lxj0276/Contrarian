# -*- coding: UTF-8 -*-
'''
@ Author: Kasper
Created on Sunday, March 24, 2019
Contrarian Strategy Backtest
'''

import os
path = os.getcwd()
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from Contrarian import get_strategy_monthly_return
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import ffn

def backtest(
    start, 
    end, 
    strategy_name, 
    loser=False, 
    winner=False, 
    small=True, 
    large=False, 
    rank_time=3, 
    hold_time=1, 
    limit=100, 
    priority="market_capital", 
    multiplier=2, 
    ST=False, 
    equity=True, 
    benchmark=True, 
    excess_return=True, 
    transaction_cost=True, 
    equity_plot=True, 
    profit_plot=True
):
    start_date = dt.strptime(start, '%Y-%m')
    end_date = dt.strptime(end, '%Y-%m')
    time_span = relativedelta(end_date, start_date).years*12 + relativedelta(end_date, start_date).months

    if not os.path.isfile(path + "\\Contrarian Result\\%s.csv" % strategy_name):
        backtest_data = pd.DataFrame()
        for date in [(dt.strptime(start, '%Y-%m') + relativedelta(months=i)).strftime('%Y-%m') for i in range(time_span)]:
            print(date, ":")
            next_df = get_strategy_monthly_return(
                start_time=date, 
                loser=loser, 
                winner=winner, 
                small=small, 
                large=large, 
                rank_time=rank_time, 
                hold_time=hold_time, 
                limit=limit, 
                priority=priority, 
                multiplier=multiplier, 
                ST=ST
            )
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
            backtest_data["Equity"] = ((backtest_data["Profit"]+1) * 0.998**2).cumprod()
            if "Benchmark Profit" in backtest_data.columns:
                backtest_data["Benchmark Equity"] = ((backtest_data["Benchmark Profit"]+1) * 0.998**2).cumprod()
        else:
            backtest_data["Equity"] = (backtest_data["Profit"]+1).cumprod()
            if "Benchmark Profit" in backtest_data.columns:
                backtest_data["Benchmark Equity"] = (backtest_data["Benchmark Profit"]+1).cumprod()
        print("回测完成，数据已保存至本地。")
        backtest_data.to_csv(path + "\\Contrarian Result\\%s.csv" % strategy_name)
    else:
        backtest_data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % strategy_name, index_col=[0])
        backtest_data.index = pd.to_datetime(backtest_data.index, format='%Y-%m')
    
    CAGR = round(((backtest_data["Equity"].iloc[-1])**(1/(time_span/12)) - 1) * 100, 3)
    print("策略年化复合增长率为%s" % CAGR + "%。")

    if equity_plot:
        equity_plot_filepath = path + "\\Contrarian Result\\%s.png" % strategy_name
        if not os.path.isfile(equity_plot_filepath):
            plt.figure(figsize=(8, 5))
            plt.plot(backtest_data.index, backtest_data["Equity"], label="Equity")
            plt.plot(backtest_data.index, backtest_data["Benchmark Equity"], label="Benchmark Equity")
            plt.legend()
            plt.title("Strategy Equity V.S. HS300 Equity")
            plt.savefig(equity_plot_filepath)
    if profit_plot:
        profit_plot_filepath = path + "\\Contrarian Result\\%s.png" % strategy_name
        if not os.path.isfile(profit_plot_filepath):
            plt.figure(figsize=(8, 5))
            plt.plot(backtest_data.index, backtest_data["Profit"], label="Profit")
            plt.plot(backtest_data.index, backtest_data["Benchmark Profit"], label="Benchmark Profit")
            plt.plot(backtest_data.index, backtest_data["Excess Return"], label="Excess Return")
            plt.legend()
            plt.title("Strategy Profit V.S. HS300 Profit")
            plt.savefig(profit_plot_filepath)

    return backtest_data