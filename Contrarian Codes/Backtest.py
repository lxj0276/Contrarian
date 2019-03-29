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

def get_file_name(
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
    market_capital="total", 
    trade_volume=False
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
            if multiplier != 2:
                strategy_name_list.append(str(multiplier))
    if ST:
        strategy_name_list.append("includeST")
    if market_capital != "total":
        strategy_name_list.append(market_capital)
    if trade_volume:
        strategy_name_list.append("with_trade_volume")
    return ' '.join(strategy_name_list)

def backtest(
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
    market_capital="total", 
    trade_volume=False
):
    strategy_name = get_file_name(
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
        market_capital=market_capital, 
        trade_volume=trade_volume
    )

    start_date = dt.strptime(start, '%Y-%m')
    end_date = dt.strptime(end, '%Y-%m')
    time_span = relativedelta(end_date, start_date).years*12 + relativedelta(end_date, start_date).months

    if not os.path.isfile(path + "\\Contrarian Result\\%s.csv" % strategy_name):
        backtest_data = pd.DataFrame()
        for date in [(dt.strptime(start, '%Y-%m') + relativedelta(months=i)).strftime('%Y-%m') for i in range(0, time_span, hold_time)]:
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
                ST=ST, 
                market_capital=market_capital, 
                trade_volume=trade_volume
            )
            backtest_data = pd.concat(
                [backtest_data, next_df], 
                axis=0
            )
    else:
        backtest_data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % strategy_name, index_col=[0])
        backtest_data.index = pd.to_datetime(backtest_data.index, format='%Y-%m')
    
    backtest_data.to_csv(path + "\\Contrarian Result\\%s.csv" % strategy_name)    
    print("回测完成，收益率数据已保存在%s文件里。" % strategy_name)

    return backtest_data