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
import statsmodels.tsa.vector_ar.vecm as vec
import GetTradingDates

numDays = 250
listDates = GetTradingDates.getDates(numDays)
listDates.reverse()

listFiles = []
listClosePrices = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    listFiles.append(file)
masterLength = numDays
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
                tempList.append((row[0],float(row[5]),file.split("\\")[1].split(".")[0]))
            if len(tempList) > masterLength:
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
# Extract each closing price for corresponding date
print("Extracting closing price per date")
counter = 0
for item in tempListPrices:
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

print("Number of stocks read: " + str(len(listClosePrices)))
listADF = []
listHalflife = []
for x in range(0,len(listClosePrices)-1):
    print(x)
    print(len(listHalflife))
    for y in range(x+1,len(listClosePrices)):
        list1 = listClosePrices[x][0]
        list2 = listClosePrices[y][0]
        model = sm.OLS(list1, list2)
        # model = sm.OLS(list1,list2)
        hedgeRatio = model.fit().params[0]
        portfolio = []
        for i in range(0, len(list1)):
            portfolio.append(list1[i] - hedgeRatio * list2[i])
        # for i in range(0,len(list1)):
        #     portfolio.append(list1[i]-hedgeRatio*list2[i])
        adf = st.adfuller(portfolio)
        if adf[0] < -3.2:
            average = statistics.mean(portfolio)
            stdv = abs(100 * statistics.stdev(portfolio) / average)
            if stdv > 500:
                portfolio2 = []
                for item in portfolio:
                    portfolio2.append(item)
                portfolio2.sort(reverse=True)
                highest = statistics.mean(portfolio2[0:20])
                lowest = statistics.mean(portfolio2[len(portfolio)-20:len(portfolio)])
                df = pd.DataFrame({'y': list1, 'x': list2})
                result = coint_johansen(df, 0, 1)
                theta = result.eig[0]
                half_life = math.log(2) / theta
                difference = highest-lowest
                realDiff = 100 * difference / statistics.mean(listClosePrices[x][0])
                if realDiff < 50 and half_life < 10:
                    peaks = []
                    valleys = []
                    for i in range(5,len(portfolio)-5):
                        if portfolio[i] >= max(portfolio[i-5:i+5]):
                            peaks.append(portfolio[i])
                        elif portfolio[i] <= min(portfolio[i-5:i+5]):
                            valleys.append(portfolio[i])
                    peaks.sort(reverse=True)
                    valleys.sort()
                    peaksvalleysstdv = 0
                    if len(peaks) >=5 and len(valleys) >=5:
                        peaksvalleysstdv = abs(statistics.stdev(peaks[0:5])/statistics.mean(peaks[0:5])) + abs(statistics.stdev(valleys[0:5])/statistics.mean(valleys[0:5]))
                        peaksvalleysstdv = 100*peaksvalleysstdv
                    if difference > 1 and peaksvalleysstdv < 70:
                        totalDistance = 0
                        for i in range(0,len(portfolio)-1):
                            totalDistance = totalDistance + abs(portfolio[i]-portfolio[i+1])
                        totalDistance = totalDistance/difference
                        #if (abs(portfolio[-1] - average) > abs(portfolio[-2] - average)) and (abs(portfolio[-1] - average) < abs(portfolio[-3] - average)):
                            #potential = round(100 * abs(portfolio[-1] - average) / list1[-1], 2)
                        listHalflife.append((listClosePrices[x][1],listClosePrices[y][1],round(adf[0],1),half_life,realDiff,stdv,peaksvalleysstdv,totalDistance))
listHalflife.sort(key=itemgetter(7),reverse=True)
for item in listHalflife:
    print(item)
exit()
listHalflife.sort(key=itemgetter(2,3))
for item in listHalflife[0:500]:
    print(item)