import os; path = os.getcwd()
import pandas as pd

for strategy in ["Loser", "Small"]:
    for limit in range(0, 501, 10):
        file_name = " ".join([strategy, str(limit)])
        data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % file_name, index_col=[0])
        data.index = pd.to_datetime(data.index, format="%Y-%m-%d").strftime('%Y-%m')
        data.index = pd.to_datetime(data.index, format='%Y-%m')
        data.to_csv(path + "\\Contrarian Result\\%s.csv" % file_name)

for limit in range(100, 201, 20):
    for method in ["intersection", "market_capital", "profit"]:
        if method == "intersection":
            file_name = " ".join(["Loser", "Small", str(limit), "intersection"])
        else:
            file_name = " ".join(["Loser", "Small", str(limit), method, "2"])
        data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % file_name, index_col=[0])
        data.index = pd.to_datetime(data.index, format="%Y-%m-%d").strftime('%Y-%m')
        data.index = pd.to_datetime(data.index, format='%Y-%m')
        data.to_csv(path + "\\Contrarian Result\\%s.csv" % file_name)