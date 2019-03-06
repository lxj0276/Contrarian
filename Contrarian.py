# -*- coding: utf-8 -*-
'''
@ Author: Kasper
Created on Tuesday, March 5, 2019
Contrarian Strategy
'''

#%%
import pandas as pd
import os
path = os.getcwd()
import datetime as dt
from dateutil.relativedelta import relativedelta
from math import floor
# import numpy as np
# import itertools
# from scipy import stats
# import seaborn as sns
# sns.set(style="darkgrid")
# import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False

#%%
class Data(object):
    '''
    Parameter:
        type: data type. (str)
            month: "month" or "m"
            year: "year" or "y"
    Attributes:
        key_word: time (month, year, etc). (str)
        date_format: time format. (str)
        key_letter: first letter of key_word. (str)
        time_label: column name of time. (str)
        return_label: column name of return. (str)
        data: data of certain type. (pd.DataFrame)       
    '''
    def __init__(self, type):

        if type == "month" or "m":
            self.key_word = "month"
            self.date_format = '%m/%d/%Y'

        elif type == "year" or "y":
            self.key_word = "year"
            self.date_format = '%Y'
    
        self.key_letter = self.key_word[0]
        self.time_label = "Trd%snt" % self.key_letter
        self.return_label = "%sretwd" % self.key_letter.capitalize()
        self.market_value_label = "%ssmvttl" % self.key_letter.capitalize()

        self.data = pd.read_csv(
            path + "\\Contrarian Data\\%s\\%s.csv" % (
                self.key_word, 
                self.key_word    
            )
        )
        self.data[self.time_label] = pd.to_datetime(
            self.data[self.time_label], 
            format = self.date_format
        )

#%%
# Apply an instance of Data class. 
Data = Data("m") # use monthly data

#%%
class Other_Data(object):
    '''
    Attributes:
        st_data: ST data. (pd.DataFrame)
        st_list: ST stocks codes list. (int64 list)
        list_data: stocks' listing data. (pd.DataFrame)
    '''
    def __init__(self):
        self.st_data = pd.read_csv(
            path + "\\Contrarian Data\\ST\\ST.csv"
        )
        self.st_list = list(self.st_data["Stkcd"].unique())
        self.list_data = pd.read_csv(
            path + "\\Contrarian Data\\list\\list.csv"
        )

#%%
def time_delta(base_time, delta_time):
    '''
    Parameters:
        base_time: base time. (str)
            month: "YYYY-MM"
            year: "YYYY"
        delta_time: how long away from base time. (int)
    Return:
        the time delta-time away from base time. (str)
    '''
    if len(base_time) == 7: # if month
        new_time = (dt.datetime.strptime(base_time, '%Y-%m') \
            + relativedelta(months=delta_time)).strftime('%Y-%m')
    elif len(base_time) == 4: # if year
        new_time = str(int(base_time) + delta_time)
    return new_time

#%%
def data_within_period(base_time, rank_time):
    '''
    Parameters:
        base_time: base time. (str)
            month: "YYYY-MM"
            year: "YYYY"
        rank_time: rank time. (int)
    Return:
        data within specified period. (pd.DataFrame)
    '''
    if rank_time > 0:
        start_time = time_delta(base_time, 0-1)
        end_time = time_delta(base_time, rank_time)
    elif rank_time <= 0:
        start_time = time_delta(base_time, rank_time-1)
        end_time = time_delta(base_time, 0)

    # Get data during specified period. 
    return Data.data[
        (Data.data[Data.time_label] > start_time) \
        & (Data.data[Data.time_label] < end_time)
    ]

#%%
class Strategy(object):
    '''
    Parameters:
        base_time: base time. (str)
            month: "YYYY-MM"
            year: "YYYY"
        rank_time: rank time. (int)
        hold_time: hold time. (int)
        limit: top & bottom limit to define winner & loser. (int)
        percentage: top & bottom percentage to define winner & loser. (float)
        small: whether trade the smallest firms only. (bool)
        large: whether trade the largest firms only. (bool)
    Attributes:
        rank_data: rank data within period, ascending sorted. (pd.DataFrame)
        hold_data: hold data within period, ascending sorted. (pd.DataFrame)
        hold_time: same as hold_time parameter. (int)
        winner: winner stocks codes list. (str list)
        loser: loser stocks codes list. (str list)
    Methods:
    '''
    def __init__(
        self, 
        base_time="2014-03", 
        rank_time=3, 
        hold_time=1, 
        limit=0, 
        percentage=0.2, 
        small=True, 
        large=False, 
        ST=False, 
    ):

        self.rank_data = data_within_period(
            base_time, -rank_time
        )

        rank_return_data = self.rank_data\
            .groupby("Stkcd")[Data.return_label]\
                .sum().sort_values()

        rank_market_value_data = self.rank_data\
            .groupby("Stkcd")[Data.market_value_label]\
                .sum().sort_values()

        self.hold_data = data_within_period(
            base_time, hold_time
        )
        self.rank_time = rank_time
        self.hold_time = hold_time
        self.limit = limit
        self.percentage = percentage
        self.small = small
        self.large = large
        self.ST = ST

        # Generate winner&loser list base on rank data.
        
        all_data_length = len(rank_return_data)

        if limit != 0:
            length = limit
        elif percentage:
            length = floor(all_data_length * percentage)
        
        self.winner = list(rank_return_data.index[-length:])
        self.loser = list(rank_return_data.index[:length])
        
        if not small or large:
            pass
        elif small:
            small_stocks_list = list(rank_market_value_data.index[:length])
            self.winner = list(set(small_stocks_list)\
                .intersection(self.winner))
            self.loser = list(set(small_stocks_list)\
                .intersection(self.loser))
        elif large:
            large_stocks_list = list(rank_market_value_data.index[-length:])
            self.winner = list(set(large_stocks_list)\
                .intersection(self.winner))
            self.loser = list(set(large_stocks_list)\
                .intersection(self.loser))
            
        if not ST:
            self.winner = [
                x for x in self.winner if x not in Other_Data().st_list
            ]
            self.loser = [
                x for x in self.loser if x not in Other_Data().st_list
            ]
    
    def rank_winner_data(self):
        '''
        Return winner data during rank period. (pd.DataFrame)
        '''
        return self.rank_data[self.rank_data["Stkcd"].isin(self.winner)]

    def rank_loser_data(self):
        '''
        Return loser data during rank period. (pd.DataFrame)
        '''
        return self.rank_data[self.rank_data["Stkcd"].isin(self.loser)]
    
    def rank_winner_return(self):
        '''
        Return winner average return during rank period. (pd.DataFrame)
        '''
        return pd.DataFrame(
            self.rank_winner_data()\
                .groupby(Data.time_label)\
                    [Data.return_label].mean()
        )
    
    def rank_loser_return(self):
        '''
        Return loser average return during rank period. (pd.DataFrame)
        '''
        return pd.DataFrame(
            self.rank_loser_data()\
                .groupby(Data.time_label)\
                    [Data.return_label].mean()
        )
    
    def hold_winner_data(self):
        '''
        Return winner data during hold period. (pd.DataFrame)
        '''
        return self.hold_data[self.hold_data["Stkcd"].isin(self.winner)]
    
    def hold_loser_data(self):
        '''
        Return loser data during hold period. (pd.DataFrame)
        '''
        return self.hold_data[self.hold_data["Stkcd"].isin(self.loser)]
    
    def hold_winner_return(self):
        '''
        Return winner average return during rank period. (pd.DataFrame)
        '''
        return pd.DataFrame(
            self.hold_winner_data()\
                .groupby(Data.time_label)\
                    [Data.return_label].mean()
        )
    
    def hold_loser_return(self):
        '''
        Return loser average return during rank period. (pd.DataFrame)
        '''
        return pd.DataFrame(
            self.hold_loser_data()\
                .groupby(Data.time_label)\
                    [Data.return_label].mean()
        )

#%%
def backtest(
    start="2018-09", 
    end="2019-02", 
    rank_time=3, 
    hold_time=1, 
    limit=0, 
    percentage=0.2, 
    small=True, 
    large=False
):
    return_dataframe = Strategy(
        start, rank_time, hold_time
    ).hold_loser_return()
    
    last_date = return_dataframe.index[-1]
    end_date = pd.to_datetime(end)

    while last_date < end_date:
        last_date = last_date.strftime("%Y-%m")
        next_start_time = time_delta(last_date, 1)
        next_return_dataframe = Strategy(
            next_start_time, rank_time, hold_time
        ).hold_loser_return()
        return_dataframe = pd.concat([
            return_dataframe, 
            next_return_dataframe
        ])
        last_date = return_dataframe.index[-1]
    
    return_dataframe["Equity"] = (return_dataframe + 1)\
        .cumprod()*100
    
    return return_dataframe

#%%
def cumulated_return(backtest):
    equity = backtest["Equity"]
    return (equity[-1]/equity[0]) - 1

#%%
backtest = backtest()

#%%
cumulated_return(backtest)

#%%
cum_prod = (backtest["Mretwd"]+1).cumprod()
cum_prod[-1] - cum_prod[0]

#%%
