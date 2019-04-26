import os; path = os.getcwd()
import pandas as pd

for strategy in ["Loser", "Small"]:
    for limit in range(0, 501, 10):
        old_file_name = " ".join([strategy, str(limit), "0901-1901"])
        try:
            os.remove(path + "\\Contrarian Result\\%s.csv" % old_file_name)
        except FileNotFoundError:
            pass
    
for limit in range(100, 201, 20):
    for method in ["intersection", "market_capital", "profit"]:
        if method == "intersection":
            old_file_name = " ".join(["Loser", "Small", str(limit), "intersection", "0901-1901"])
        else:
            old_file_name = " ".join(["Loser", "Small", str(limit), method, "2", "0901-1901"])
    try:
        os.remove(path + "\\Contrarian Result\\%s.csv" % old_file_name)
    except FileNotFoundError:
        pass