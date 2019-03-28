# -*- coding: UTF-8 -*-
'''
@ Author: Kasper
Created on Wednesday, March 27, 2019
Contrarian Strategy Analysis
'''
import os; path = os.getcwd()
import pandas as pd
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import ffn

    equity=True, 
    benchmark=True, 
    excess_return=True, 
    transaction_cost=True, 
    equity_plot=False, 
    profit_plot=False, 
    performance_report=True

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