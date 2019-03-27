# -*- coding: UTF-8 -*-
'''
@ Author: Kasper
Created on Tuesday, March 5, 2019
Contrarian Strategy
'''
import os
path = os.getcwd()
import itertools
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from functools import partial

raw_data = pd.read_csv(path + "\\Contrarian Data\\month\\month.csv")
time_label = "Trdmnt"
market_capital_label = "Msmvttl"
profit_label = "Mretwd"
time_format = '%m/%d/%Y'
raw_data[time_label] = pd.to_datetime(raw_data[time_label], format=time_format)

def get_aggregate_data(base_time, delta_time, groupby_label="Stkcd", calculate_label=profit_label, portfolio_list=[]):
    if delta_time > 0:
        start = (dt.strptime(base_time, '%Y-%m') + relativedelta(months=-1)).strftime('%Y-%m')
        end = (dt.strptime(base_time, '%Y-%m') + relativedelta(months=delta_time)).strftime('%Y-%m')
    elif delta_time <= 0:
        start = (dt.strptime(base_time, '%Y-%m') + relativedelta(months=delta_time-1)).strftime('%Y-%m')
        end = (dt.strptime(base_time, '%Y-%m') + relativedelta(months=0)).strftime('%Y-%m')
    data = raw_data[(raw_data[time_label] > start) & (raw_data[time_label] < end)].dropna()
    if len(portfolio_list) != 0:
        data = data[data["Stkcd"].isin(portfolio_list)]
    return data.groupby(groupby_label)[calculate_label]

def get_strategy_monthly_return(
    start_time, 
    loser=True, 
    winner=False, 
    small=True, 
    large=False, 
    rank_time=3, 
    hold_time=1, 
    limit=100, 
    priority="market_capital", 
    multiplier=2, 
    ST=False
):

    if loser or winner:
        rank_profit_data = get_aggregate_data(
            base_time=start_time, 
            delta_time=-rank_time
        ).sum().sort_values()
    
    if small or large:
        rank_market_capital_data = get_aggregate_data(
            base_time=start_time, 
            delta_time=-rank_time, 
            calculate_label=market_capital_label
        ).sum().sort_values()

    # 选择投资组合。
    global portfolio_list

    if (loser or winner) and not (small or large):
        if loser:
            portfolio_list = list(rank_profit_data.index[:limit])
        elif winner:
            portfolio_list = list(rank_profit_data.index[-limit:])

    if (small or large) and not (loser or winner):
        if small:
            portfolio_list = list(rank_market_capital_data.index[:limit])
        elif large:
            portfolio_list = list(rank_market_capital_data.index[-limit:])

    if (loser or winner) and (small or large):

        # 二者取交集。
        if priority == "intersection":
            if loser:
                profit_list = list(rank_profit_data.index[:limit])
            elif winner:
                profit_list = list(rank_profit_data.index[-limit:])
            if small:
                market_capital_list = list(rank_market_capital_data.index[:limit])
            elif large:
                market_capital_list = list(rank_market_capital_data.index[-limit:])
            portfolio_list = set(profit_list).intersection(market_capital_list)

        # 收益优先。
        elif priority == "profit":
            if loser:
                profit_list = list(rank_profit_data.index[:limit*multiplier])
            elif winner:
                profit_list = list(rank_profit_data.index[-limit*multiplier:])
            rank_market_capital_data = get_aggregate_data(
                base_time=start_time, 
                delta_time=-rank_time, 
                calculate_label=market_capital_label, 
                portfolio_list=profit_list
            ).sum().sort_values()
            if small:
                portfolio_list = list(rank_market_capital_data.index[:limit])
            elif large:
                portfolio_list = list(rank_market_capital_data.index[-limit:])
        
        # 市值优先。
        elif priority == "market_capital":
            if small:
                market_capital_list = list(rank_market_capital_data.index[:limit*multiplier])
            elif large:
                market_capital_list = list(rank_market_capital_data.index[-limit*multiplier:])
            rank_profit_data = get_aggregate_data(
                base_time=start_time, 
                delta_time=-rank_time, 
                portfolio_list=market_capital_list
            ).sum().sort_values()
            if loser:
                portfolio_list = list(rank_profit_data.index[:limit])
            elif winner:
                portfolio_list = list(rank_profit_data.index[-limit:])
    
    if not ST:
        ST_list = list(pd.read_csv(path+"\\Contrarian Data\\ST\\ST.csv")["Stkcd"].unique())
        portfolio_list = [x for x in portfolio_list if x not in ST_list]
    
    hold_return_data = pd.DataFrame(get_aggregate_data(
        base_time=start_time, 
        delta_time=hold_time, 
        groupby_label=time_label, 
        calculate_label=profit_label, 
        portfolio_list=portfolio_list        
    ).mean())
    # 假如当月投资组合为空，则收益为零。
    if hold_return_data.empty:
        datetime_index = [(dt.strptime(start_time, '%Y-%m') + relativedelta(months=i)) for i in range(hold_time)]
        hold_return_data = pd.DataFrame(
            data=list(itertools.repeat(0, hold_time)), 
            index=pd.to_datetime(datetime_index)
        )
    hold_return_data.index.name = "Month"
    hold_return_data.columns = ["Profit"]

    return hold_return_data