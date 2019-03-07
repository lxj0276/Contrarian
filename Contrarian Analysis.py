# -*- coding: utf-8 -*-
'''
@ Author: Kasper
Created on Thursday, March 7, 2019
Contrarian Strategy
'''

#%%
#%%
def report_dataframe(backtest_dataframe):
    report_dataframe = pd.DataFrame(
        index = ["Report"], 
        columns = list(backtest_dataframe.columns)
    )

    report_dataframe[Data.return_label][0] \
        = backtest_dataframe[Data.return_label].mean()
    report_dataframe["Equity"][0] \
        = (backtest_dataframe["Equity"][-1]/100) - 1
    report_dataframe["Benchmark"][0] \
        = (backtest_dataframe["Benchmark"][-1]/100) - 1
    
    return backtest_dataframe.append(report_dataframe)