import os; path = os.getcwd()
import pandas as pd
os.chdir(path + "\\Contrarian Result")

for i in range(0, 201, 20):
    os.rename("Loser Small %s profit 2.csv" % str(i), "Loser Small %s profit.csv" % str(i))

for i in range(0, 501, 10):
    os.rename("Loser Small %s market_capital 2.csv" % str(i), "Loser Small %s market_capital.csv" % str(i))