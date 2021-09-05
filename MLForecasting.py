import random

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
import scipy
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import GetTradingDates

outputList = []
numDays = 2500
listDates = GetTradingDates.getDates(numDays)
listDates.reverse()

listFiles = []
listClosePrices = []
tempListPrices = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    listFiles.append(file)
for file in listFiles:
    tempList = []
    try:
        with open(file, "r") as inputfile:
            csvreader = csv.reader(inputfile)
            header = next(csvreader)
            for row in csvreader:
                tempList.append((row[0],float(row[5]),file.split("\\")[1].split(".")[0]))
            if len(tempList) > numDays:
                tempList.reverse()
                tempListPrices.append(tempList)
                #listClosePrices.append((tempList[len(tempList)-masterLength:len(tempList)],file.split("\\")[1].split(".")[0]))

    except:
        print("blank: " + str(file))
print(len(tempListPrices))

# Check for duplicate dates
for item in tempListPrices:
    tempdates = []
    for x in item:
        tempdates.append(x[0])
    if len(tempdates) != len(set(tempdates)):
        print("duplicates in " + str(item[2]))
        exit()
print("Extracting closing price per date")
counter = 0
for item in tempListPrices[0:100]:
    counter = counter + 1
    print(counter)
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

outputList.append(("Current distance to mean","1 year ADF", "2 year ADF", "5 year ADF", "Half-life", "1 year stdv", "Days since intersecting mean","Change in distance tomorrow"))
stockPairIndexList = []
for x in range(0,len(listClosePrices)):
    for y in range(x+1,len(listClosePrices)):
        stockPairIndexList.append((x,y))
random.shuffle(stockPairIndexList)
for item in stockPairIndexList:
    print(item)
pairIndex = 0
print("Length of stock pair list: "+str(len(stockPairIndexList)))
while len(outputList) < 10000 and pairIndex < len(stockPairIndexList):
    x = stockPairIndexList[pairIndex][0]
    y = stockPairIndexList[pairIndex][1]
    print(pairIndex)
    print(x)
    print(y)
    print(len(outputList))
    print("---------------------------------")
    fullList1 = listClosePrices[x][0]
    fullList2 = listClosePrices[y][0]
    #year 1
    list1 = fullList1[0:1250]
    list2 = fullList2[0:1250]
    list1shorter = fullList1[750:1250]
    list2shorter = fullList2[750:1250]
    list1shortest = fullList1[1000:1250]
    list2shortest = fullList2[1000:1250]
    portfolioshortest = []
    portfolioshorter = []
    portfolio = []
    model = sm.OLS(list1shortest,list2shortest)
    hedgeRatio = model.fit().params[0]
    for i in range(0, len(list1shortest)):
        portfolio.append(list1shortest[i] - hedgeRatio * list2shortest[i])
    adf1 = st.adfuller(portfolio)
    if adf1[0] < -3:
        portfolio2 = []
        model = sm.OLS(list1shorter, list2shorter)
        hedgeRatio2 = model.fit().params[0]
        for i in range(0, len(list1shorter)):
            portfolio2.append(list1shorter[i] - hedgeRatio2 * list2shorter[i])
        adf2 = st.adfuller(portfolio2)
        if adf2[0] < -2.9:
            portfolio3 = []
            model = sm.OLS(list1, list2)
            hedgeRatio3 = model.fit().params[0]
            for i in range(0, len(list1)):
                portfolio3.append(list1[i] - hedgeRatio3 * list2[i])
            adf3 = st.adfuller(portfolio3)
            if adf3[0] < -2.8:
                df = pd.DataFrame({'y': list1shortest, 'x': list2shortest})
                result = coint_johansen(df, 0, 1)
                theta = result.eig[0]
                half_life = math.log(2) / theta
                half_life = round(half_life) - 6
                portfolio4 = []
                average = statistics.mean(portfolio)
                stdv = statistics.stdev(portfolio)/abs(average)
                crossings = []
                for i in range(1250,1500):
                    portfolio4.append(fullList1[i]-hedgeRatio*fullList2[i])
                if portfolio4[0] > average:
                    higherorlower = 0
                else:
                    higherorlower = 1
                for i in range(1,250):
                    if higherorlower == 1 and portfolio4[i] > average:
                        crossings.append(i)
                        higherorlower = 0
                    elif higherorlower == 0 and portfolio4[i] < average:
                        crossings.append(i)
                        higherorlower = 1
                if len(crossings) > 4:
                    for i in range(min(crossings),min(max(crossings),249)):
                        tempDaysSinceIntersectionList = []
                        for item in crossings:
                            if i - item >= 0:
                                tempDaysSinceIntersectionList.append(i-item)

                        outputList.append((abs(portfolio4[i]-average),adf1[0],adf2[0],adf3[0],half_life,stdv,min(tempDaysSinceIntersectionList),abs(portfolio4[i+1]-average)-abs(portfolio4[i]-average)))
    pairIndex = pairIndex + 1
np.savetxt("test.csv",outputList,delimiter=",",fmt='% s')
exit()
#year 2
list1 = listClosePrices[x][250:1500]
list2 = listClosePrices[y][250:1500]
list1shorter = listClosePrices[x][1000:1500]
list2shorter = listClosePrices[y][1000:1500]
list1shortest = listClosePrices[x][1250:1500]
list2shortest = listClosePrices[y][1250:1500]

#year 3
list1 = listClosePrices[x][500:1750]
list2 = listClosePrices[y][500:1750]
list1shorter = listClosePrices[x][1250:1750]
list2shorter = listClosePrices[y][1250:1750]
list1shortest = listClosePrices[x][1500:1750]
list2shortest = listClosePrices[y][1500:1750]
