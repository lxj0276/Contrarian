# -*- coding: utf-8 -*-
'''
@ Author: Kasper
Created on Friday, March 8, 2019
Contrarian Strategy Analysis
'''

#%%
import pandas as pd
import os
path = os.getcwd()
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from Contrarian import Strategy, data_within_period
from Contrarian import Other_Data
import ffn

#%%
def get_backtest_data(*args):
    '''
    Parameters: 
    ------------
    *args: words in strategy name. (str list)
    Return:
    --------
    backtest return data of the strategy. (pd.DataFrame)
    '''
    strategy_name = ' '.join(args)
    file_path = path + "\\Contrarian Result\\%s.csv" % strategy_name
    data = pd.read_csv(
        path + "\\Contrarian Result\\%s.csv" % strategy_name, 
        index_col=[0]
    )
    data.index = pd.to_datetime(data.index, format="%Y-%m-%d")
    return data

#%%
def report_dataframe(
    backtest_data, 
    start="2018-01", 
    end="2019-01", 
    transaction_cost=False
):
    '''
    Parameters:
    -----------
    backtest_data: backtest return data. (pd.DataFrame)
    transaction_cost: whether transaction cost. (bool)
    start: start time. 
    end: end time. 
    Return:
    -------
    monthly-return and equity of strategy and benchmark. (pd.DataFrame)
    '''
    start = pd.to_datetime(start, format='%Y-%m')
    end = pd.to_datetime(end, format='%Y-%m')
    report = backtest_data[
        (backtest_data.index > start) & (backtest_data.index < end)
    ].copy()
    report.columns = ["Strategy Return"]

    if transaction_cost:
        report["Strategy Equity"] = \
            ((report + 1) * 0.998**2).cumprod() * 100
    else:
        report["Strategy Equity"] = \
            (report + 1).cumprod() * 100

    hs300 = Other_Data().hs300
    report["Benchmark Return"] = list(
        hs300[hs300["Month"].isin(list(
            report.index.strftime("%Y-%m")
        ))]["Idxrtn"]
    )
    report["Benchmark Equity"] = \
        (report["Benchmark Return"] + 1).cumprod() * 100
    
    report["Excess Return"] = report["Strategy Return"] - report["Benchmark Return"]

    return report


#%%
def print_CAGR(*args):
    final_equity = report_dataframe(
        backtest_data=get_backtest_data(args), 
        start="2008-12", 
        end="2019-01", 
        transaction_cost=True
    )["Strategy Equity"][-1]
    CAGR = (final_equity/100)**(1/10)-1
    print(CAGR)

#%%
def get_value_data(limit):
    return report_dataframe(
        backtest_data=get_backtest_data(*[
            "0901-1902", 
            "Loser", 
            "Small", 
            str(limit), 
            "value"
        ]), 
        start="2008-12", 
        end="2019-01", 
        transaction_cost=True
    )

#%%
def save_all_equity():
    all_equity = get_value_data(5)[[
        "Benchmark Equity", 
        "Strategy Equity"
    ]]
    all_equity.columns = ["Benchmark", "5"]
    for i in list(range(50, 201, 10)) + [250, 300]:
        data = pd.DataFrame(get_value_data(i)["Strategy Equity"])
        data.columns = [str(i)]
        all_equity = pd.concat(
            [all_equity, data], 
            axis=1
        )
    all_equity.to_excel(
        path + "\\Contrarian Result\\All Equity (value).xlsx", 
        sheet_name="Equity"
    )

#%%
def volatility_research():
    data = report_dataframe(
        backtest_data=get_backtest_data(*[
            "0901-1902", 
            "Small", 
            "150"
        ]), 
        start="2008-12", 
        end="2019-01", 
        transaction_cost=True
    )
    data.to_excel(
        path + "\\Contrarian Result\\150 Small.xlsx", 
        sheet_name="Report"
    )

    #%%
    data = report_dataframe(
        backtest_data=get_backtest_data(*[
            "0901-1902", 
            "Loser", 
            "Small", 
            "100", 
            "intersection"
        ]), 
        start="2008-12", 
        end="2019-01", 
        transaction_cost=True
    )
    month_list = [x.strftime(format="%Y-%m") for x in data.index]

    #%%
    portfolio_record = pd.DataFrame(
        index = data.index, 
        columns = [
            "Portfolio Amount", 
            "Portfolio"
        ]
    )
    for i in month_list:
        portfolio = Strategy().get_portfolio(i)
        amount = len(portfolio)
        portfolio_record.loc[
            pd.to_datetime(i, format="%Y-%m"), 
            "Portfolio Amount"
        ] = amount
        portfolio_record.loc[
            pd.to_datetime(i, format="%Y-%m"), 
            "Portfolio"
        ] = portfolio
    portfolio_record

    #%%
    volatility = portfolio_record
    volatility_list = []
    for i in month_list:
        data = data_within_period(i, -3).dropna()
        data = data[data["Stkcd"].isin(
            volatility.loc[
                pd.to_datetime(i, format="%Y-%m"), 
                "Portfolio"
            ]
        )]
        volatility_list.append(
            (data.groupby("Trdmnt")["Mnshrtrd"].mean()).mean()
        )
    volatility["Volatility"] = volatility_list

    #%%
    data = pd.concat([
        data, 
        pd.DataFrame(volatility[["Portfolio Amount", "Volatility"]])
    ], axis=1)
    data.to_excel(
        path + "\\Contrarian Result\\Volatility Research.xlsx", 
        sheet_name="Data"
    )

#%%
def trade_volume(data):

    #%%
    data = pd.read_excel(
        path + "\\Contrarian Result\\Volatility Research.xlsx", 
        index_col = [0]
    )

    data["MA3 of Vol"] = list(data["Volatility"].rolling(3).apply(
        lambda x: x.mean(), 
        raw=True
    ))
    data.fillna(0, inplace=True)

    #%%
    data["0.88MA3"] = 0.88 * data["MA3 of Vol"]

    #%%
    adjust_ret_list = []
    for i in range(len(data)):
        if data["MA3 of Vol"].iloc[i] \
            < data["0.88MA3"].iloc[i]:
            adjust_ret_list.append(0)
        else:
            adjust_ret_list.append(
                data["Strategy Return"].iloc[i]
            )
    data["Adjusted Return"] = adjust_ret_list

    #%%
    data["Adjusted Equity"] = (data["Adjusted Return"] + 1).cumprod() * 100

    #%%
    data.to_excel(
        path + "\\Contrarian Result\\Volatility Research.xlsx", 
        sheet_name="Volatility Research"
    )

#%%
data = report_dataframe(
    backtest_data=get_backtest_data(*[
        "0901-1902", 
        "Small", 
        "150"
    ]), 
    start="2008-12", 
    end="2019-01", 
    transaction_cost=True
)

#%%
adjusted_return_list = [0]
for i in range(1, len(data)):
    previous_return = data["Strategy Return"].iloc[i-1]
    if previous_return > 0:
        adjusted_return_list.append(
            data["Strategy Return"].iloc[i]
        )
    else:
        adjusted_return_list.append(0)
data["Adjusted Return"] = adjusted_return_list
data["Adjusted Equity"] = (data["Adjusted Return"]+1).cumprod() * 100

#%%
data.to_excel(
    path + "\\Contrarian Result\\Simple Stop Loss.xlsx", 
    sheet_name="Stop Loss"
)

#%%
