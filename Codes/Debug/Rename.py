import os; path = os.getcwd()
import pandas as pd

for strategy in ["Loser", "Small"]:
    for limit in range(0, 501, 10):
        old_file_name = " ".join([strategy, str(limit), "0901-1901"])
        data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % old_file_name, index_col=[0])
        new_file_name = " ".join([strategy, str(limit)])
        data.to_csv(path + "\\Contrarian Result\\%s.csv" % new_file_name)

    
for limit in range(100, 201, 20):
    for method in ["intersection", "market_capital", "profit"]:
        if method == "intersection":
            old_file_name = " ".join(["Loser", "Small", str(limit), "intersection", "0901-1901"])
            new_file_name = " ".join(["Loser", "Small", str(limit), "intersection"])
        else:
            old_file_name = " ".join(["Loser", "Small", str(limit), method, "2", "0901-1901"])
            new_file_name = " ".join(["Loser", "Small", str(limit), method, "2"])
    data = pd.read_csv(path + "\\Contrarian Result\\%s.csv" % old_file_name, index_col=[0])
    data.to_csv(path + "\\Contrarian Result\\%s.csv" % new_file_name)