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
listDates = GetTradingDates.getDates(numDays)
listDates.reverse()
# with open("C:/Users/17132/PycharmProjects/pythonProject/Crypto/BTC.csv","r") as btcFile:
#     csvreader = csv.reader(btcFile)
#     header = next(csvreader)
#     for row in csvreader:
#         btcPrices.append(float(row[3]))
# with open("C:/Users/17132/PycharmProjects/pythonProject/Crypto/ETH.csv","r") as ethFile:
#     csvreader = csv.reader(ethFile)
#     header = next(csvreader)
#     for row in csvreader:
#         ethPrices.append(float(row[3]))
# ethPrices.reverse()
# btcPrices.reverse()

listFiles = []
listClosePrices = []
betaList = []

currentPairs = 0

if currentPairs == 0:
    #file = "C:/Users/17132/Desktop/Weekly List of Long Term Cointegrated/Long Term Cointegrated - Sep 3.txt"
    file2 = "C:/Users/17132/Desktop/Weekly List of Long Term Cointegrated/Long Term Cointegrated - Sep 6.txt"
    #file3 = "C:/Users/17132/Desktop/Weekly List of Long Term Cointegrated/Long Term Cointegrated - Sep 2.txt"
    file3 = ""
    file = ""
else:
    file = "C:/Users/17132/Desktop/Current Pairs.txt"
listStocks = []
listPairs = []
try:
    with open(file, "r") as inputfile:
        try:
            while 1==1:
                line = inputfile.readline()
                equityA = line.split(",")[0].replace("'","").replace("(","").strip()
                equityB = line.split(",")[1].replace("'","").replace(")","").strip()
                avghalflife = line.split(",")[2].replace(")","").strip()
                listStocks.append(equityB)
                listStocks.append(equityA)
                listPairs.append((equityA,equityB))
        except:
            pass
except:
    pass
if currentPairs == 0:
    with open(file2, "r") as inputfile:
        try:
            while 1==1:
                line = inputfile.readline()
                equityA = line.split(",")[0].replace("'","").replace("(","").strip()
                equityB = line.split(",")[1].replace("'","").replace(")","").strip()
                avghalflife = line.split(",")[2].replace(")","").strip()
                listStocks.append(equityB)
                listStocks.append(equityA)
                listPairs.append((equityA,equityB))
        except:
            pass
    try:
        with open(file3, "r") as inputfile:
            try:
                while 1==1:
                    line = inputfile.readline()
                    equityA = line.split(",")[0].replace("'","").replace("(","").strip()
                    equityB = line.split(",")[1].replace("'","").replace(")","").strip()
                    avghalflife = line.split(",")[2].replace(")","").strip()
                    listStocks.append(equityB)
                    listStocks.append(equityA)
                    listPairs.append((equityA,equityB))
            except:
                pass
    except:
        pass
print("Num stocks read: " + str(len(listStocks)))
listStocks = set(listStocks)
print("Num unique stocks read: " + str(len(listStocks)))
print("Num pairs read: " + str(len(listPairs)))
listPairs = set(listPairs)
print("Num unique pairs read: " + str(len(listPairs)))
for stock in listStocks:
   if os.path.isfile("C:/Users/17132/PycharmProjects/pythonProject/ETFs/"+stock+".csv"):
        listFiles.append("C:/Users/17132/PycharmProjects/pythonProject/ETFs/"+stock+".csv")
   elif os.path.isfile("C:/Users/17132/PycharmProjects/pythonProject/Stocks/" + stock + ".csv"):
        listFiles.append("C:/Users/17132/PycharmProjects/pythonProject/Stocks/" + stock + ".csv")
print(len(listFiles))

dates = []
tempListPrices = []
for file in listFiles:
    tempList = []
    try:
        with open(file, "r") as inputfile:
            csvreader = csv.reader(inputfile)
            header = next(csvreader)
            for row in csvreader:
                tempList.append((row[0],float(row[5]),file.split("/")[6].split(".")[0]))
            tempList.reverse()
            tempListPrices.append(tempList)
    except:
        print("blank: " + str(file))



# Check for duplicate dates
for item in tempListPrices:
    tempdates = []
    for x in item:
        tempdates.append(x[0])
    if len(tempdates) != len(set(tempdates)):
        print("duplicates in " + str(item[2]))
        exit()
# Extract each closing price for corresponding date
counter = 0
excludedCounter = 0
for item in tempListPrices:
    print(counter)
    counter = counter + 1
    listPrices = []
    for date in listDates:
        found = False
        index = 0
        while found is False and index < len(item):
            if str(item[index][0]) == str(date):
                listPrices.append(item[index][1])
                found = True
            index = index + 1
        if found is False and len(listPrices) > 0:
            listPrices.append(listPrices[-1])
    if len(listPrices) == numDays:
        # betaScore = -9999
        ticker = item[2][2]
        # for item in betaList:
        #     if ticker == item[0] and betaScore == -999:
        #         betaScore = item[1]
        # if betaScore == -9999:
        #     print(ticker)
        #     print("Ticker not found in beta list.")

#        listClosePrices.append((listPrices,ticker,betaScore))
        listClosePrices.append((listPrices,ticker))


print("Number of stocks read: " + str(len(listClosePrices)))
summaryList = []
print("Number of pairs read: " + str(len(listPairs)))
for item in listPairs:
    try:
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
        list1s = list1[250:500]
        list2s = list2[250:500]
        list1t = list1
        list2t = list2
        list1 = list1s
        list2 = list2s
        model = sm.OLS(list1,list2)
        hedgeRatio = model.fit().params[0]
        portfolio = []
        for i in range(0,len(list1)):
            portfolio.append(list1[i] - hedgeRatio*list2[i])
        adf = st.adfuller(portfolio)

        #print(adf[0])
        average = statistics.mean(portfolio)
        df = pd.DataFrame({'y': list1t, 'x': list2t})
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
        print(spreadapart)

        if currentPairs == 0:
            #if (0 < half_life < 25 and spreadapart > 1.2 and (abs(portfolio[-1]-average)> abs(portfolio[-2]-average)) and (abs(portfolio[-1]-average) < abs(portfolio[-3]-average))):
            # if abs(portfolio[-1]-average) < abs(portfolio[-3]-average):
            if (0 < half_life < 25 and spreadapart > 1.2):
                summaryList.append((listClosePrices[x][1],listClosePrices[y][1],round(half_life)-6,spreadapart,round(adf[0],2),potential,round(50*potential/half_life,2)))
            else:
                excludedCounter = excludedCounter + 1
        else:
            summaryList.append((listClosePrices[x][1], listClosePrices[y][1], round(half_life) - 6, spreadapart,
                                round(adf[0], 2), potential, round(50 * potential / half_life, 2)))
    except:
        pass

#summaryList.sort(key=itemgetter(2,3))
summaryList.sort(key=itemgetter(6),reverse=True)
for item in summaryList[0:300]:
    print(item)





