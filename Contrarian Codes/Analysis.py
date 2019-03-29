# -*- coding: UTF-8 -*-
'''
@ Author: Kasper
Created on Wednesday, March 27, 2019
Contrarian Strategy Analysis
'''
import os; path = os.getcwd()
from Backtest import get_file_name, backtest
import pandas as pd
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import ffn

def analysis(
    loser=True, 
    winner=False, 
    small=True, 
    large=False, 
    rank_time=3, 
    hold_time=1, 
    limit=100, 
    priority="market_capital", 
    multiplier=2, 
    start="2009-01", 
    end="2019-01", 
    ST=False, 
    market_capital="total", 
    equity=True, 
    benchmark=True, 
    excess_return=True, 
    transaction_cost=True, 
    performance_report=True, 
    store_data=False
):
    file_name = get_file_name(
        start=start, 
        end=end, 
        loser=loser, 
        winner=winner, 
        small=small, 
        large=large, 
        rank_time=rank_time, 
        hold_time=hold_time, 
        limit=limit, 
        priority=priority, 
        multiplier=multiplier, 
        ST=ST, 
        market_capital=market_capital
    )
    if os.path.isfile(path + "\\Contrarian Result\\%s.csv" % file_name):
        data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % file_name, index_col=[0])
        data.index = pd.to_datetime(data.index)
    else:
        data = backtest(
            start=start, 
            end=end, 
            loser=loser, 
            winner=winner, 
            small=small, 
            large=large, 
            rank_time=rank_time, 
            hold_time=hold_time, 
            limit=limit, 
            priority=priority, 
            multiplier=multiplier, 
            ST=ST, 
            market_capital=market_capital
        )
    
    if benchmark:
        # 获取benchmark数据，这里是沪深300.
        hs300 = pd.read_csv(path + "\\Contrarian Data\\benchmark\\benchmark.csv")
        hs300 = hs300[hs300["Indexcd"] == 300]
        hs300 = hs300[["Month", "Idxrtn"]]
        hs300.set_index("Month", inplace=True)
        hs300.columns = ["Benchmark Profit"]
        hs300.index = pd.to_datetime(hs300.index)
        data = data.join(hs300)
    if excess_return:
        data["Excess Return"] = data["Profit"] - data["Benchmark Profit"]
    if equity:
        data["Equity"] = (data["Profit"]+1).cumprod()
        if "Benchmark Profit" in data.columns:
            data["Benchmark Equity"] = (data["Benchmark Profit"]+1).cumprod()
        if transaction_cost:
            data["Equity with Transaction Cost"] = ((data["Profit"]+1) * 0.998**2).cumprod()
            if "Benchmark Profit" in data.columns:
                data["Benchmark Equity with Transaction Cost"] = ((data["Benchmark Profit"]+1) * 0.998**2).cumprod()
    if store_data: 
        data.to_csv(path + "\\Contrarian Result\\%s Equity.csv" % file_name)
    
    if performance_report:
        if transaction_cost:
            performance = data["Equity with Transaction Cost"].calc_stats()
        else:
            performance = data["Equity"].calc_stats()
        print("%s 策略回测报告：" % file_name)
        print("* 年化复合增长率为%s" % round(performance.cagr*100, 3) + "%。")
        print("* 最大回撤为%s" % round(performance.max_drawdown*100, 3) + "%。")
        print("* 夏普值为%s。" % round(performance.daily_sharpe, 3))
    
    return data