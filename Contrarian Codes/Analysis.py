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
    start="2009-01", 
    end="2019-01", 
    loser=True, 
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
    equity_plot=False, 
    profit_plot=False, 
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
        ST=ST
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
            ST=ST
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

    if equity_plot:
        equity_plot_filepath = path + "\\Contrarian Result\\%s Equity.png" % file_name
        if not os.path.isfile(equity_plot_filepath):
            plt.figure(figsize=(8, 5))
            plt.plot(data.index, data["Equity"], label="Equity")
            plt.plot(data.index, data["Benchmark Equity"], label="Benchmark Equity")
            plt.legend()
            plt.title("Strategy Equity V.S. HS300 Equity")
            plt.savefig(equity_plot_filepath)
    if profit_plot:
        profit_plot_filepath = path + "\\Contrarian Result\\Profit of %s.png" % file_name
        if not os.path.isfile(profit_plot_filepath):
            plt.figure(figsize=(8, 5))
            plt.plot(data.index, data["Profit"], label="Profit")
            plt.plot(data.index, data["Benchmark Profit"], label="Benchmark Profit")
            plt.plot(data.index, data["Excess Return"], label="Excess Return")
            plt.legend()
            plt.title("Strategy Profit V.S. HS300 Profit")
            plt.savefig(profit_plot_filepath)

    if performance_report:
        performance = data["Equity"].calc_stats()
        print("策略年化复合增长率为%s" % round(performance.cagr*100, 3) + "%。")
        print("策略最大回撤为%s" % round(performance.max_drawdown*100, 3) + "%。")
        print("策略夏普值为%s" % round(performance.daily_sharpe, 3))