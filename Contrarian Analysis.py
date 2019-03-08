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

plt.figure(figsize = (12, 8))
plt.plot("Equity", data = return_dataframe, label="Strategy")
plt.plot("Benchmark", data = return_dataframe, label="HS300")
plt.legend()
plt.title("Equity of " + strategy_name)
plt.savefig(path + "\\Contrarian Report\\CTR RP Plots\\" + strategy_name + ".png")

if transaction_cost:
    return_dataframe["Equity"] = ((return_dataframe + 1)\
        * 0.998**2).cumprod() * 100
else:
    return_dataframe["Equity"] = (return_dataframe + 1)\
        .cumprod() * 100

hs300 = Other_Data().hs300
return_dataframe["Benchmark"] = list(
    hs300[hs300["Month"].isin(list(
        return_dataframe.index.strftime("%Y-%m")
    ))]["Idxrtn"])

return_dataframe["Benchmark"] = (return_dataframe["Benchmark"] + 1)\
    .cumprod() * 100