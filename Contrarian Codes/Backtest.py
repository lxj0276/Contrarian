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
    equity_plot=True, 
    profit_plot=True, 
    performance_report=True
):
    strategy_name_list = []
    if loser or winner:
        if loser:
            strategy_name_list.append("Loser")
        elif winner:
            strategy_name_list.append("Winner")
    if small or large:
        if small:
            strategy_name_list.append("Small")
        elif large:
            strategy_name_list.append("Large")
    if (rank_time != 3) and (hold_time != 1):
        strategy_name_list.append(str(rank_time) + "-" + str(hold_time))
    strategy_name_list.append(str(limit))
    if (loser or winner) and (small or large):
        strategy_name_list.append(priority)
        if priority != "intersection":
            strategy_name_list.append(str(multiplier))
    if ST:
        strategy_name_list.append("includeST")
    if not transaction_cost:
        strategy_name_list.append("NoTransactionCost")
    strategy_name_list.append(start[2:4] + start[-2:] + "-" + end[2:4] + end[-2:])
    strategy_name = ' '.join(strategy_name_list)

    start_date = dt.strptime(start, '%Y-%m')
    end_date = dt.strptime(end, '%Y-%m')
    time_span = relativedelta(end_date, start_date).years*12 + relativedelta(end_date, start_date).months

    if not os.path.isfile(path + "\\Contrarian Result\\%s.csv" % strategy_name):
        backtest_data = pd.DataFrame()
        for date in [(dt.strptime(start, '%Y-%m') + relativedelta(months=i)).strftime('%Y-%m') for i in range(0, time_span, hold_time)]:
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
            hs300 = hs300[hs300["Indexcd"] == 300]
            hs300 = hs300[["Month", "Idxrtn"]]
            hs300.set_index("Month", inplace=True)
            hs300.columns = ["Benchmark Profit"]
            hs300.index = pd.to_datetime(hs300.index, format='%Y-%m')
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

    if equity_plot:
        equity_plot_filepath = path + "\\Contrarian Result\\Equity of %s.png" % strategy_name
        if not os.path.isfile(equity_plot_filepath):
            plt.figure(figsize=(8, 5))
            plt.plot(backtest_data.index, backtest_data["Equity"], label="Equity")
            plt.plot(backtest_data.index, backtest_data["Benchmark Equity"], label="Benchmark Equity")
            plt.legend()
            plt.title("Strategy Equity V.S. HS300 Equity")
            plt.savefig(equity_plot_filepath)
    if profit_plot:
        profit_plot_filepath = path + "\\Contrarian Result\\Profit of %s.png" % strategy_name
        if not os.path.isfile(profit_plot_filepath):
            plt.figure(figsize=(8, 5))
            plt.plot(backtest_data.index, backtest_data["Profit"], label="Profit")
            plt.plot(backtest_data.index, backtest_data["Benchmark Profit"], label="Benchmark Profit")
            plt.plot(backtest_data.index, backtest_data["Excess Return"], label="Excess Return")
            plt.legend()
            plt.title("Strategy Profit V.S. HS300 Profit")
            plt.savefig(profit_plot_filepath)

    if performance_report:
        performance = backtest_data["Equity"].calc_stats()
        print("策略年化复合增长率为%s" % round(performance.cagr*100, 3) + "%。")
        print("策略最大回撤为%s" % round(performance.max_drawdown*100, 3) + "%。")
        print("策略夏普值为%s" % round(performance.daily_sharpe, 3))

    return backtest_data