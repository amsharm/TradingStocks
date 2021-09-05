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

numDays = 1500
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
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    listFiles.append(file)

dates = []
tempListPrices = []
for file in listFiles:
    tempList = []
    #try:
    with open(file, "r") as inputfile:
        csvreader = csv.reader(inputfile)
        header = next(csvreader)
        print(file)
        for row in csvreader:
            tempList.append((row[0],float(row[5]),file.split("\\")[1].split(".")[0]))
        tempList.reverse()
        if len(tempList) > numDays and tempList[2][2] != "GE":
            tempListPrices.append(tempList)
    #except:
        #print("blank: " + str(file))

print(len(tempListPrices))

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
        listClosePrices.append((listPrices,item[2][2]))



print("Number of stocks read: " + str(len(listClosePrices)))
summaryList = []

for x in range(0,len(listClosePrices)-1):
    print(x)
    print(len(summaryList))
    for y in range(x+1,len(listClosePrices)):
        try:
            list1 = listClosePrices[x][0]
            list2 = listClosePrices[y][0]
            model = sm.OLS(list1,list2)
            hedgeRatio = model.fit().params[0]
            portfolio = []
            for i in range(0,len(list1)):
                portfolio.append(list1[i] - hedgeRatio*list2[i])
            adf = st.adfuller(portfolio)
            if adf[0] < -2:
                summaryList.append((listClosePrices[x][1],listClosePrices[y][1], adf[0]))
        except:
            pass

summaryList.sort(key=itemgetter(2))
for item in summaryList[0:300]:
    print(item)





