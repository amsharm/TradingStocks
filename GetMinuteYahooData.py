import glob
import time
import yfinance as yf
import pandas as pd
import datetime as dt
def exec():
    # Set the start and end date
    start_date = '2021-07-13'
    end_date = '2021-08-04'
    # Set the ticker
    tickerList = ["VGSH", "VOO", "SPLG", "IVV", "SCHO"]


    for ticker in tickerList:
        print(ticker)
        data = yf.download(tickers=ticker, start=start_date, end=end_date,interval="5m")
        df = pd.DataFrame(data)
        df.to_csv("C:/Users/17132/PycharmProjects/pythonProject/MinuteData/"+str(ticker)+".csv")

