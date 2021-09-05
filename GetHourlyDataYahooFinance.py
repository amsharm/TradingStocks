import glob
import time
import yfinance as yf
import pandas as pd
import datetime as dt
from datetime import timedelta

# Set the start and end date
start_date = dt.date.today() - timedelta(days=50)
end_date = dt.date.today() + timedelta(days=1)


#ticker = yf.Ticker("SPY")
#data = yf.download(ticker, start_date, end_date)
#data = ticker.history(start=start_date,end=end_date, interval="5m")
#df = pd.DataFrame(data)
#df.to_csv("C:/Users/17132/PycharmProjects/pythonProject/Hourly Data/SPY.csv")
#exit()
print("End date: " + str(end_date))
# Set the ticker
tickerList = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    tickerList.append(file.split("\\")[1].split(".")[0])
for ticker in tickerList:
    print(ticker)

    hourTicker = yf.Ticker(ticker)
    data = hourTicker.history(start=start_date, end=end_date, interval="5m")
    df = pd.DataFrame(data)
    df.to_csv("C:/Users/17132/PycharmProjects/pythonProject/Hourly Data/"+str(ticker)+".csv")

    #time.sleep(1)

tickerList = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    tickerList.append(file.split("\\")[1].split(".")[0])
for ticker in tickerList:
    print(ticker)

    hourTicker = yf.Ticker(ticker)
    data = hourTicker.history(start=start_date, end=end_date, interval="5m")
    df = pd.DataFrame(data)
    df.to_csv("C:/Users/17132/PycharmProjects/pythonProject/Hourly Data/"+str(ticker)+".csv")

    #time.sleep(1)