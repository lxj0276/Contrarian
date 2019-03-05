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
import numpy as np
import itertools
from scipy import stats
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

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
def timedelta(base_time, delta_time):
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
    start_time = timedelta(base_time, rank_time)
    end_time = timedelta(base_time, 1)

    # Get data during specified period. 
    return Data.data[
        (Data.data[Data.time_label] > start_time) \
        & (Data.data[Data.time_label] < end_time)
    ]

#%%
def aggregate_data_sum(data_to_aggregate, label):
    '''
    Parameter:
        data_to_aggregate: 
            data to be calculated it's
            aggregate return of each stocks. (pd.DataFrame)
        label: label of column to aggregate on. (str)
    Return:
        aggregate sum of each stocks specified column, 
        ascending sorted. (pd.DataFrame)
    '''
    # Sum up return of each stocks during rank period. 
    aggregate_data_sum = data_to_aggregate\
        .groupby("Stkcd")[label].sum()
    # Sort values in ascending order.
    return aggregate_data_sum.sort_values()

#%%
class Rank(object):
    '''
    Parameters:
        base_time: base time. (str)
            month: "YYYY-MM"
            year: "YYYY"
        rank_time: rank time. (int)
        limit: top & bottom limit to define winner & loser. (int)
        percentage: top & bottom percentage to define winner & loser. (float)
    Attributes:
        data: data within period, ascending sorted. (pd.DataFrame)
        return_data: cumulated return data of each stocks. (pd.Series)
        winner: winner stocks codes list. (str list)
        loser: loser stocks codes list. (str list)
    Methods:
    '''
    def __init__(
        self, 
        base_time, 
        rank_time, 
        limit=0, 
        percentage=0.2, 
        small=True, 
        large=False
    ):
        self.data = data_within_period(
            base_time, rank_time
        )
        return_data = aggregate_data_sum(
            self.data, 
            Data.return_label
        )
        market_value_data = aggregate_data_sum(
            self.data, 
            Data.market_value_label
        )
        
        all_data_length = len(return_data)

        if limit != 0:
            length = limit
        elif percentage:
            length = floor(all_data_length * percentage)
        
        self.winner = list(return_data.index[-length:])
        self.loser = list(return_data.index[:length])
        
        if not small or large:
            pass
        elif small:
            small_stocks_list = list(market_value_data.index[:length])
            self.winner = set(small_stocks_list).intersection(self.winner)
            self.loser = set(small_stocks_list).intersection(self.loser)
        elif large:
            large_stocks_list = list(market_value_data.index[-length:])
            self.winner = set(large_stocks_list).intersection(self.winner)
            self.loser = set(large_stocks_list).intersection(self.loser)
    
    def winner_data(self):
        return self.data[self.data["Stkcd"].isin(self.winner)]

    def loser_data(self):
        return self.data[self.data["Stkcd"].isin(self.loser)]

#%%
