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
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#%%
class Raw_Data(object):
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
        self.trade_label = "%snshrtrd" % self.key_letter.capitalize()

        file_path = path + "\\Contrarian Data\\%s\\%s" \
            % (self.key_word, self.key_word)

        if os.path.isfile(file_path + ".h5"):
            data_store = pd.HDFStore(file_path + ".h5")
            self.data = data_store[self.key_word] # 40 ns
            data_store.close()
        
        else:
            self.data = pd.read_csv(file_path + ".csv")
            self.data[self.time_label] = pd.to_datetime(
                self.data[self.time_label], 
                format = self.date_format
            )
            data_store = pd.HDFStore(file_path + ".h5")
            data_store[self.key_word] = self.data
            data_store.close()

#%%
Data = Raw_Data("m")

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
        self.benchmark = pd.read_csv(
            path + "\\Contrarian Data\\benchmark\\benchmark.csv"
        )
        self.szzs = self.benchmark[self.benchmark["Indexcd"] == 1]
        self.hs300 = self.benchmark[self.benchmark["Indexcd"] == 300]

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
def time_span(start, end):
    '''
    Parameters:
    ----------
    start: start time. (str)
    end: end time. (str)

    Return: 
    ------
    time span. (int)
    '''
    start_date = dt.datetime.strptime(start, '%Y-%m')
    end_date = dt.datetime.strptime(end, '%Y-%m')
    length = relativedelta(end_date, start_date).years * 12 + \
    relativedelta(end_date, start_date).months
    return length

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
        start: start time. (str)
        end: end time. (str)
        rank_time: rank time. (int)
        hold_time: hold time. (int)
        limit: top & bottom limit to define winner & loser. (int)
        loser: whether trade loser. (bool)
        winner: whether trade winner. (bool)
        small: whether trade the smallest firms only. (bool)
        large: whether trade the largest firms only. (bool)
        ST: whether trade ST stocks. (bool)
        priority:
            how to deal with intersection. (str)
            - "intersection": simply intersect both. 
            - "return": 
                first take <2*limit> of return rank portfolio, 
                then take <limit> value-rank of them as portfolio. 
            - "value": same as "return" but rank value first. 
    Methods: 
        get_rank_data(base_time): 
            Parameter: 
                base_time: base time. (str)
            Return: data during rank period. (pd.DataFrame)
        get_hold_data(base_time):
            Return data during hold period. (pd.DataFrame)
        rank_data(rank_data, by):
            Parameters:
                rank_data: data to rank. (pd.DataFrame)
                by: column to sum on. (Data.attribute)
            Return: ranked data. (pd.DataFrame)
        get_return_portfolio(base_time, multiplier)
            Parameters:
                multiplier: how many times limit. 
            loser or winner portfolio. 
        get_value_portfolio(base_time, multiplier)
            Parameters:
                multiplier: how many times limit. 
            small or large portfolio. 
        get_portfolio(base_time)
            Return: final portfolios on base time. (int list)
        get_hold_return(base_time)
            Return: average return during rank period. (pd.DataFrame)
        backtest(strategy_name, transaction_cost)
            Parameters:
                strategy_name: 
                    name of the strategy. (str)
                    also name of csv/png file
                transaction_cost: whether trade cost. (bool)
    '''
    def __init__(
        self, 
        start="2018-01", 
        end="2019-02", 
        rank_time=3, 
        hold_time=1, 
        limit=100, 
        loser=True, 
        winner=False, 
        small=True, 
        large=False, 
        ST=False, 
        priority="intersection"
    ):
        self.start = start
        self.end = end
        self.rank_time = rank_time
        self.hold_time = hold_time
        self.limit = limit
        self.loser = loser
        self.winner = winner
        self.small = small
        self.large = large
        self.ST = ST
        self.priority = priority
    
    def get_rank_data(self, base_time): 
        return data_within_period(base_time, -self.rank_time)
    
    def get_hold_data(self, base_time):
        data = data_within_period(base_time, self.hold_time)
        return data[data["Stkcd"].isin(self.get_portfolio(base_time))]
    
    def rank_data(self, rank_data, by=Data.return_label):
        return rank_data.groupby("Stkcd")[by].sum().sort_values()
    
    def get_return_portfolio(self, base_time, multiplier=1):
        data = self.rank_data(
            self.get_rank_data(base_time), 
            by=Data.return_label
        )
        if self.loser:
            return list(data.index[:self.limit*multiplier])
        elif self.winner:
            return list(data.index[-self.limit*multiplier:])

    def get_value_portfolio(self, base_time, multiplier=1):
        data = self.rank_data(
            self.get_rank_data(base_time), 
            by=Data.market_value_label
        )
        if self.small:
            return list(data.index[:self.limit*multiplier])
        elif self.large:
            return list(data.index[-self.limit*multiplier:])            
    
    def get_portfolio(self, base_time): # 35 ms

        if (self.loser or self.winner) and (self.small or self.large):

            if self.priority == "intersection":
                p1 = self.get_return_portfolio(base_time)
                p2 = self.get_value_portfolio(base_time)
                portfolio = list(set(p1).intersection(p2))

            elif self.priority == "return":
                p1 = self.get_return_portfolio(base_time, 2)
                data = self.get_rank_data(base_time)
                data = data[data["Stkcd"].isin(p1)]
                data = self.rank_data(data, Data.market_value_label)

                if self.small:
                    portfolio = list(data.index[:self.limit])

                elif self.large:
                    portfolio = list(data.index[-self.limit:])
                    
            elif self.priority == "value":
                p1 = self.get_value_portfolio(base_time, 2)
                data = self.get_rank_data(base_time)
                data = data[data["Stkcd"].isin(p1)]
                data = self.rank_data(data, Data.return_label)

                if self.loser:
                    portfolio = list(data.index[:self.limit])

                elif self.winner:
                    portfolio = list(data.index[-self.limit:])
        
        elif (self.loser or self.winner) or (self.small or self.large):

            if self.loser or self.winner:
                portfolio = self.get_return_portfolio(base_time)

            elif self.small or self.large:
                portfolio = self.get_value_portfolio(base_time)

        if not self.ST:
            portfolio = [
                x for x in portfolio if x not in Other_Data().st_list
            ]
        
        return portfolio

    def get_hold_return(self, base_time): # 11 ms
        return pd.DataFrame(
            self.get_hold_data(base_time).groupby(Data.time_label)\
                [Data.return_label].mean()
        )
    
    def get_date_list(self): 
        return [time_delta(self.start, i) for i in list(
                range(0, time_span(
                    self.start, self.end
                ), self.hold_time)
            )]
    
    def backtest(
        self, 
        strategy_name="Contrarian"
    ):
        return_dataframe = pd.DataFrame()
        for date in self.get_date_list():
            next_return_dataframe = self.get_hold_return(date)
            return_dataframe = return_dataframe.append(next_return_dataframe)
        return_dataframe.to_csv(
            path + "\\Contrarian Report\\CTR RP Data\\" + strategy_name + ".csv"
        )
        return return_dataframe

#%%
strategy = Strategy(
    start="2009-01", 
    end="2019-02", 
    rank_time=3, 
    hold_time=1, 
    limit=100, 
    loser=False, 
    winner=True, 
    small=False, 
    large=True, 
    ST=False, 
    priority="intersection"
)

#%%
strategy.backtest(strategy_name="0901-1902 Loser Small 100 intersection")