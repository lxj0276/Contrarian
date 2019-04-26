# -*- coding: UTF-8 -*-
import os; path = os.getcwd()
import pandas as pd

hs300 = pd.read_csv(path + "\\Contrarian Data\\benchmark\\benchmark.csv")
hs300 = hs300[hs300["Indexcd"] == 300]
hs300 = hs300[["Month", "Idxrtn"]]
hs300.set_index("Month", inplace=True)
hs300.columns = ["Benchmark Profit"]
hs300.index = pd.to_datetime(hs300.index, format='%Y-%m')

for limit in range(0, 501, 10):
    file_name = " ".join(["Loser", str(limit), "0901-1901"])
    data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % file_name, index_col=[0])
    data = data[["Profit", "Equity"]]
    data = data.join(hs300)
    data["Excess Return"] = data["Profit"] - data["Benchmark Profit"]
    data["Benchmark Equity"] = ((data["Benchmark Profit"]+1) * 0.998**2).cumprod()
    data.to_csv(path + "\\Contrarian Result\\%s.csv" % file_name)

for limit in range(0, 501, 10):
    file_name = " ".join(["Small", str(limit), "0901-1901"])
    data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % file_name, index_col=[0])
    data = data[["Profit", "Equity"]]
    data = data.join(hs300)
    data["Excess Return"] = data["Profit"] - data["Benchmark Profit"]
    data["Benchmark Equity"] = ((data["Benchmark Profit"]+1) * 0.998**2).cumprod()
    data.to_csv(path + "\\Contrarian Result\\%s.csv" % file_name)
    
for limit in range(100, 201, 20):
    for method in ["intersection", "market_capital", "profit"]:
        if method == "intersection":
            file_name = " ".join(["Loser", "Small", str(limit), "intersection", "0901-1901"])
        else:
            file_name = " ".join(["Loser", "Small", str(limit), method, "2", "0901-1901"])
        file_name = " ".join(["Small", str(limit), "0901-1901"])
    data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % file_name, index_col=[0])
    data = data[["Profit", "Equity"]]
    data = data.join(hs300)
    data["Excess Return"] = data["Profit"] - data["Benchmark Profit"]
    data["Benchmark Equity"] = ((data["Benchmark Profit"]+1) * 0.998**2).cumprod()
    data.to_csv(path + "\\Contrarian Result\\%s.csv" % file_name)