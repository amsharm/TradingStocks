import statsmodels.tsa.stattools as st
import math
import statistics
import csv
import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import os.path
import pandas as pd
import xlrd
import statsmodels.api as sm
import sys
sys.path.append("..")
from johansen import coint_johansen
import GetTradingDates

numDays = 500



listFiles = []
listClosePrices = []

file = "C:/Users/17132/Desktop/Hourly Long Term Cointegrated/Aug 31.txt"
listStocks = []
listPairs = []
with open(file, "r") as inputfile:
    try:
        while 1==1:
            line = inputfile.readline()
            equityA = line.split(",")[0].replace("'","").replace("(","").strip()
            equityB = line.split(",")[1].replace("'","").replace(")","").strip()
            avghalflife = line.split(",")[2].replace(")","").strip()
            listStocks.append(equityB)
            listStocks.append(equityA)
            listPairs.append((equityA,equityB,avghalflife))
    except:
        pass
print(len(listStocks))
listStocks = set(listStocks)
for stock in listStocks:
    listFiles.append("C:/Users/17132/PycharmProjects/pythonProject/Hourly Data/" + stock + ".csv")
print(len(listFiles))

dates = []
tempListPrices = []
for file in listFiles:
    print(file)
    tempList = []
    try:
        with open(file, "r") as inputfile:
            csvreader = csv.reader(inputfile)
            header = next(csvreader)
            for row in csvreader:
                try:
                    tempList.append(float(row[4]))
                except:
                    pass
            if len(tempList) == 2219:
                listClosePrices.append((tempList[len(tempList)-500:len(tempList)],file.split("/")[6].split(".")[0]))
    except:
        print("blank: " + str(file))


print("Number of stocks read: " + str(len(listClosePrices)))
summaryList = []
print("Number of pairs read: " + str(len(listPairs)))
for item in listPairs:
    #try:
    x = 0
    y = 0
    print(item[0])
    print(item[1])
    while listClosePrices[x][1] != item[0]:
        x = x + 1
    while listClosePrices[y][1] != item[1]:
        y = y + 1
    print("First stock: " + str(x) + " " + item[0])
    print("Second stock: " + str(y) + " " + item[1])


    list1 = listClosePrices[x][0]
    list2 = listClosePrices[y][0]
    model = sm.OLS(list1,list2)
    hedgeRatio = model.fit().params[0]
    portfolio = []
    for i in range(0,len(list1)):
        portfolio.append(list1[i] - hedgeRatio*list2[i])
    adf = st.adfuller(portfolio)

    #print(adf[0])
    average = statistics.mean(portfolio)
    df = pd.DataFrame({'y': list1, 'x': list2})
    result = coint_johansen(df, 0, 1)
    theta = result.eig[0]
    half_life = math.log(2) / theta
    #half_life = round(half_life) - 6
    spreadapart = round(abs(portfolio[-1]-average)/statistics.stdev(portfolio),2)
    distribution = round(abs(statistics.stdev(portfolio)/average),2)
    potential = round(100*abs(portfolio[-1]-average)/list1[-1],2)
    # if portfolio[-1] < average:
    #     betaDiff = listClosePrices[y][2]-listClosePrices[x][2]
    # else:
    #     betaDiff = listClosePrices[x][2]-listClosePrices[y][2]
    print(half_life)
    #if (0 < half_life < 25 and spreadapart > 1.2) or half_life < 5:
    summaryList.append((listClosePrices[x][1],listClosePrices[y][1],round(half_life)-6,spreadapart,round(adf[0],2),potential,round(100*potential/half_life,2),item[2]))
    #except:
        #pass

#summaryList.sort(key=itemgetter(2,3))
summaryList.sort(key=itemgetter(2))
for item in summaryList[0:300]:
    print(item)





