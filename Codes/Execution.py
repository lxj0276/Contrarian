from Backtest import backtest
from Analysis import analysis
import os; path = os.getcwd()
import pandas as pd
import ffn

# # 尝试6-1是否确实比3-1强。
# analysis(rank_time=3)
# analysis(rank_time=6)

# # 研究超级严格的止损，只要交易量下降下个月就空仓。
# original_data = analysis(limit=30)
# data = analysis(limit=30, trade_volume=True, stop_loss="trade_volume")
# for i in range(1, len(data)):
#     if data["Trade Volume"].iloc[i] < data["Trade Volume"].iloc[i-1]:
#         data["Profit"].iloc[i] = 0
# data["Equity of Strict Stop Loss"] = ((data["Profit"]+1) * 0.998**2).cumprod()
# original_performance = original_data["Equity with Transaction Cost"].calc_stats()
# stop_loss_performance = data["Equity with Transaction Cost"].calc_stats()
# strict_performance = data["Equity of Strict Stop Loss"].calc_stats()
# report_data = pd.DataFrame(index=["原始策略", "止损策略", "严格止损"], columns=["复合年化收益率", "日波动率", "夏普比率", "最大回撤", "平均回撤", "平均回撤时长（日）"])
# report_data.loc["原始策略", "复合年化收益率"] = original_performance.cagr
# report_data.loc["止损策略", "复合年化收益率"] = stop_loss_performance.cagr
# report_data.loc["严格止损", "复合年化收益率"] = strict_performance.cagr
# report_data.loc["原始策略", "日波动率"] = original_performance.daily_vol
# report_data.loc["止损策略", "日波动率"] = stop_loss_performance.daily_vol
# report_data.loc["严格止损", "日波动率"] = strict_performance.daily_vol
# report_data.loc["原始策略", "夏普比率"] = original_performance.daily_sharpe
# report_data.loc["止损策略", "夏普比率"] = stop_loss_performance.daily_sharpe
# report_data.loc["严格止损", "夏普比率"] = strict_performance.daily_sharpe
# report_data.loc["原始策略", "最大回撤"] = original_performance.max_drawdown
# report_data.loc["止损策略", "最大回撤"] = stop_loss_performance.max_drawdown
# report_data.loc["严格止损", "最大回撤"] = strict_performance.max_drawdown
# report_data.loc["原始策略", "平均回撤"] = original_performance.avg_drawdown
# report_data.loc["止损策略", "平均回撤"] = stop_loss_performance.avg_drawdown
# report_data.loc["严格止损", "平均回撤"] = strict_performance.avg_drawdown
# report_data.loc["原始策略", "平均回撤时长（日）"] = original_performance.avg_drawdown_days
# report_data.loc["止损策略", "平均回撤时长（日）"] = stop_loss_performance.avg_drawdown_days
# report_data.loc["严格止损", "平均回撤时长（日）"] = strict_performance.avg_drawdown_days
# report_data.to_excel(path + "\\Analysis\\止损研究（30支股票）.xlsx")
# # 观察他们的净值。
# total_data = pd.DataFrame()
# total_data = total_data.join(original_data[["Equity with Transaction Cost"]], how="right")
# simple_data = data[["Equity with Transaction Cost"]]
# simple_data.columns = ["Equity of Stop Loss"]
# total_data = total_data.join(simple_data, how="right")
# total_data = total_data.join(data[["Equity of Strict Stop Loss"]], how="right")
# total_data.to_excel(path + "\\Analysis\\止损净值展示（30支股票）.xlsx")

# # 交易量预测止损的相关性研究。
# total_data = pd.DataFrame(index=range(10, 201, 10), columns=["Correlation Coefficient", "P Value"])
# for i in range(10, 201, 10):
#     data = backtest(limit=i, trade_volume=True)
#     data["Previous Profit"] = data["Profit"].shift(1)
#     data.dropna(inplace=True)
#     from scipy.stats import pearsonr
#     result = pearsonr(data["Trade Volume"], data["Previous Profit"])
#     total_data.loc[i, "Correlation Coefficient"] = result[0] 
#     total_data.loc[i, "P Value"] = result[1]
# total_data.to_excel(path + "\\Analysis\\交易量预测的相关性.xlsx")

# # 交易量预测的调参。
# total_data = pd.DataFrame(index=[x/100 for x in range(50, 101, 2)])
# for i in [x/100 for x in range(50, 101, 2)]:
#     data = analysis(limit=30, trade_volume=True, stop_loss="trade_volume", scale_down_trade_vol_par=i)
#     performance = data["Equity with Transaction Cost"].calc_stats()
#     total_data.loc[i, "复合年化收益率"] = performance.cagr
#     total_data.loc[i, "夏普比率"] = performance.daily_sharpe
#     total_data.loc[i, "波动率"] = performance.daily_vol
#     total_data.loc[i, "最大回撤"] = performance.max_drawdown
#     total_data.loc[i, "平均回撤"] = performance.avg_drawdown
#     total_data.loc[i, "平均回撤日长"] = performance.avg_drawdown_days
# total_data.to_excel(path + "\\Analysis\\交易量调参.xlsx")

# # 最终结果展示。
# total_data = pd.DataFrame(index=range(10, 201, 5))
# for i in range(10, 201, 5):
#     original_data = analysis(limit=i)
#     original_performance = original_data["Equity with Transaction Cost"].calc_stats()
#     stop_loss_data = analysis(limit=i, trade_volume=True, stop_loss="trade_volume", scale_down_trade_vol_par=0.82)
#     stop_loss_performance = stop_loss_data["Equity with Transaction Cost"].calc_stats()
#     total_data.loc[i, "原始策略复合年化收益率"] = original_performance.cagr
#     total_data.loc[i, "原始策略夏普比率"] = original_performance.daily_sharpe
#     total_data.loc[i, "原始策略波动率"] = original_performance.daily_vol
#     total_data.loc[i, "原始策略最大回撤"] = original_performance.max_drawdown
#     total_data.loc[i, "原始策略平均回撤"] = original_performance.avg_drawdown
#     total_data.loc[i, "原始策略平均回撤日长"] = original_performance.avg_drawdown_days
#     total_data.loc[i, "止损策略复合年化收益率"] = stop_loss_performance.cagr
#     total_data.loc[i, "止损策略夏普比率"] = stop_loss_performance.daily_sharpe
#     total_data.loc[i, "止损策略波动率"] = stop_loss_performance.daily_vol
#     total_data.loc[i, "止损策略最大回撤"] = stop_loss_performance.max_drawdown
#     total_data.loc[i, "止损策略平均回撤"] = stop_loss_performance.avg_drawdown
#     total_data.loc[i, "止损策略平均回撤日长"] = stop_loss_performance.avg_drawdown_days
# total_data.to_excel(path + "\\Analysis\\止损效果展示.xlsx")

# # 目前最好的一个策略。
# data = analysis(limit=30, trade_volume=True, stop_loss="trade_volume", scale_down_trade_vol_par=0.82)

# 总结对比目前最好的策略。
total_data = pd.DataFrame()
stock_amount = []
strategy_name = []
cagr = []
sharpe = []
volatility = []
max_drawdown = []
avg_drawdown = []
avg_drawdown_days = []
for strategy in ["小市值", "反转+小市值", "反转+小市值+止损"]:
    for i in range(5, 151, 5):
        if strategy == "小市值":
            data = analysis(loser=False, limit=i)
        elif strategy == "反转+小市值":
            data = analysis(limit=i)
        elif strategy == "反转+小市值+止损":
            data = analysis(limit=i, trade_volume=True, stop_loss="trade_volume", scale_down_trade_vol_par=0.82)
        performance = data["Equity with Transaction Cost"].calc_stats()
        stock_amount.append(i)
        strategy_name.append(strategy)
        cagr.append(performance.cagr)
        sharpe.append(performance.daily_sharpe)
        volatility.append(performance.daily_vol)
        max_drawdown.append(-performance.max_drawdown)
        avg_drawdown.append(-performance.avg_drawdown)
        avg_drawdown_days.append(performance.avg_drawdown_days)
total_data["股票数量"] = stock_amount
total_data["策略"] = strategy_name
total_data["复合年化收益率"] = cagr
total_data["夏普比率"] = sharpe
total_data["波动率"] = volatility
total_data["最大回撤"] = max_drawdown
total_data["平均回撤"] = avg_drawdown
total_data["平均回撤日长"] = avg_drawdown_days
total_data.to_excel(path + "\\Analysis\\策略对比(0.82).xlsx")