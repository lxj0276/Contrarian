# 2.2 更新
# 1. 更改了策略的函数名，更加直观
# 2. 将注释从英文改为中文
# 3. 

# 加载所需模块
import pandas as pd           # 数据处理
import datetime as dt         # 日期
from WindPy import *          # 万德数据API
from WindAlgo import *        # 回测
from WindCharts import *      # 绘图
w.start(show_welcome = False) # 启动万德

# 反转&小市值交易策略。

today = dt.datetime.now().strftime("%Y-%m-%d") # 今天的日期
# 今天的A股股票列表。
securities = w.wset(
	"sectorconstituent", 
	"date="+today+";sectorId=a001010100000000;field=wind_code,sec_name"
).Data[0]

def initialize(context):
	context.capital = 1e9           # 10亿元人民币作为初始资金
	context.securities = securities # A股股票列表作为证券池
	context.start_date = "20090101" # 回测在2009年01月01日开始
	context.end_date = "20171231"   # 回测在2017年12月31日结束
	context.period = "d"            # 回测频率为一天
	context.benchmark = "000300.SH" # 沪深300作为基准
	context.fields = "sec_name,windcode,pct_chg_per,mkt_cap_ashare2"
    '''
    获取指标列表：
    1. 证券名称
    2. 万德代码
    3. 涨跌幅
    4. 市值（A股市值，含限售股）
    '''
	
def handle_data(bar_datetime, context, bar_data):
	pass

def strategy(bar_datetime, context, bar_data):
    trade_date = bar_datetime.strftime("%Y-%m-%d") # 在回测的“今天”开始交易
    # 排序
	start_rank_date = w.tdaysoffset(
		-3,                                        # 在交易日的三个月之前开始排序
		trade_date, 
		"Period=M;Days=Alldays"
	).Data[0][0].strftime("%Y-%m-%d")
	end_rank_date = w.tdaysoffset(
		-1, # end rank 1 day ago
		trade_date, 
		"Period=D;Days=Alldays"
	).Data[0][0].strftime("%Y-%m-%d")
	# Data contains percentage change and market capital. 
	data = w.wss(
		context.securities, 
		context.fields, 
		"startDate="+start_rank_date+";endDate="+end_rank_date+";trade_date="+trade_date+"", 
		usedf = True # generate pandas dataframe directly
	)[1]
	data.dropna(inplace = True) # drop data not available
	data.sort_values("MKT_CAP_ASHARE2", inplace = True) # sort by market capital to select small stocks
	small_stock_list = list(data[ : round(len(data)/10)].index) # select the 10% smallest stocks in the past 3 months
	data.sort_values("PCT_CHG_PER", inplace = True) # sort by percentage change to select loser stocks
	loser_stock_list = list(data[ : round(len(data)/10)].index) # select the 10% worst performing stocks in the past 3 months
	target_list = [x for x in small_stock_list if x in loser_stock_list] # select the intersection of 10% smallest and 10% worst as our target. 
	current_stock_list = wa.query_position().get_field("code") # get the stocks list I currently hold
	buy_list = [x for x in target_list if x not in current_stock_list] # buy stocks I previously don't have but is my target
	wa.change_securities(buy_list) # change context.securities, but why won't it affect next loop?
	sell_list = [x for x in current_stock_list if x not in target_list] # sell stocks i previously have but is not my target
	continue_holding_list = [x for x in target_list if x in current_stock_list] # 
	for code in sell_list:
		volume = wa.query_position()[code]['volume'] # query how much position is in my portfolio
		res = wa.order(code, volume, "sell", price = "close", volume_check = False) # sell stocks
	for code in buy_list:
		res = wa.order_percent(code, 1/len(buy_list), 'buy', price = "close", volume_check = False) # buy stocks equally weighted
	for code in continue_holding_list:
		res = wa.order_target_percent(code, 1/len(continue_holding_list), 'buy', price = "close", volume_check = False) # incremental switching position


wa = BackTest(init_func = initialize, handle_data_func = handle_data)
wa.schedule(CTR_SCPT, "m", 0) # execute strategy on the first trading day each month
res = wa.run(show_progress = True)

def windframe_to_dataframe(windframe):
	df = pd.DataFrame()
	column_list = windframe.fields
	for column in column_list:
		df[column] = wind_frame.get_field(column)
	return df
# Backtest summary. 
result = windframe_to_dataframe(wa.summary("result"))
nav = windframe_to_dataframe(wa.summary("nav"))
trade = windframe_to_dataframe(wa.summary("trade"))
position = windframe_to_dataframe(wa.summary("position"))
monthly_profit = windframe_to_dataframe(wa.summary("monthly_profit"))
position_rate = windframe_to_dataframe(wa.summary("position_rate"))
stat_month = windframe_to_dataframe(wa.summary("stat_month"))
stat_quarter = windframe_to_dataframe(wa.summary("stat_quarter"))
stat_year = windframe_to_dataframe(wa.summary("stat_year"))