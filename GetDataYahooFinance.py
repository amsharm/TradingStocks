import glob
import time
import yfinance as yf
import pandas as pd
import datetime as dt
from datetime import timedelta

# Set the start and end date
start_date = '2011-02-01'
end_date = dt.date.today() + timedelta(days=1)
#end_date - dt.date.today()

# tickerList = ["PLTM","PPLT","PGM",]
# for ticker in tickerList:
#     data = yf.download(ticker, start_date, end_date)
#
#     df = pd.DataFrame(data)
#     df.to_csv("C:/Users/17132/PycharmProjects/pythonProject/ETFs/"+str(ticker)+".csv")
# exit()
print("End date: " + str(end_date))
# Set the ticker
tickerList = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    tickerList.append(file.split("\\")[1].split(".")[0])
for ticker in tickerList:
    print(ticker)
    try:
        data = yf.download(ticker, start_date, end_date)
        df = pd.DataFrame(data)
        df.to_csv("C:/Users/17132/PycharmProjects/pythonProject/Stocks/"+str(ticker)+".csv")
    except:
        pass
    #time.sleep(1)

tickerList = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    tickerList.append(file.split("\\")[1].split(".")[0])
for ticker in tickerList:
    print(ticker)
    try:
        data = yf.download(ticker, start_date, end_date)
        df = pd.DataFrame(data)
        df.to_csv("C:/Users/17132/PycharmProjects/pythonProject/ETFs/"+str(ticker)+".csv")
    except:
        pass
    #time.sleep(1)