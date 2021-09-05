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

listDates = GetTradingDates.getDates(250)
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
masterLength = 250
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
            tempList.reverse()
            tempListPrices.append(tempList)
            #if len(tempList) > masterLength:
                #listClosePrices.append((tempList[len(tempList)-masterLength:len(tempList)],file.split("\\")[1].split(".")[0]))

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
for item in tempListPrices:
    listPrices = []
    print(counter)
    counter = counter + 1
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
    if len(listPrices) == 250:
        listClosePrices.append((listPrices,item[2][2]))

print("Number of stocks read: " + str(len(listClosePrices)))
summaryList = []
print(len(listClosePrices[0][0]))
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
            print(adf[0])
            #if adf[0] < -3.2:
            if adf[0] < -2.9:
                df = pd.DataFrame({'y': list1, 'x': list2})
                result = coint_johansen(df, 0, 1)
                theta = result.eig[0]
                half_life = math.log(2) / theta
                half_life = round(half_life) - 6
                if half_life < 10:
                    ratiosMovingAvg5 = []
                    ratiosMovingAvg60 = []
                    ratiosStd60 = []
                    zscoreList = []
                    for i in range(60, len(portfolio)):
                        ratiosMovingAvg5.append(statistics.mean(portfolio[i - 5:i]))
                        ratiosMovingAvg60.append(statistics.mean(portfolio[i - 60:i]))
                        ratiosStd60.append(statistics.stdev(portfolio[i - 60:i]))
                    for i in range(0, len(ratiosMovingAvg5)):
                        if ratiosStd60[i] > 0:
                            zscoreList.append((ratiosMovingAvg5[i] - ratiosMovingAvg60[i]) / ratiosStd60[i])
                    validzscore = False
                    if zscoreList[-3] > 1 and zscoreList[-1] < zscoreList[-2] and zscoreList[-2] < zscoreList[-3] and zscoreList[-3] >= max(zscoreList[-13:-1]):
                        validzscore = True
                    if zscoreList[-3] < -1 and zscoreList[-1] > zscoreList[-2] and zscoreList[-2] > zscoreList[-3] and zscoreList[-3] <= min(zscoreList[-13:-1]):
                        validzscore = True
                    if validzscore == True:
                        zrateofchange = 1
                        #zrateofchange = int(100*round(abs(zscoreList[-1]-zscoreList[-3])/2,2))
                        # if 0 < zrateofchange < 40:
                        #     zrateofchange = 40 - zrateofchange
                        #     if zrateofchange < 27:
                        summaryList.append((round(zscoreList[-1],3),round(adf[0],3),round(hedgeRatio,3),half_life,zrateofchange,x,y,listClosePrices[x][1],listClosePrices[y][1],half_life+zrateofchange))
        except:
            pass

summaryList.sort(key=itemgetter(3))
for item in summaryList:
    print(item)






exit()
totalCount = 0
finalSummaryList = []
summaryList.sort(key=itemgetter(0))
for item in summaryList:
    totalCount = totalCount + 1
    print(totalCount)
    list1 = listClosePrices[item[4]][0][masterLength-250:masterLength]
    list2 = listClosePrices[item[5]][0][masterLength-250:masterLength]

    #list1 = list1[1200:1500]
    #list2 = list2[1200:1500]
    #model = sm.OLS(list1, list2)
    #hedgeRatio = model.fit().params[0]
    hedgeRatio = item[6]
    #print(hedgeRatio)
    ratioList = []
    for i in range(0, len(list1)):
        ratioList.append(list1[i] - hedgeRatio * list2[i])
    ratiosMovingAvg5 = []
    ratiosMovingAvg60 = []
    ratiosStd60 = []
    #ratioList = ratioList[1000:1500]
    zscoreList = []
    for i in range(60, len(ratioList)):
        ratiosMovingAvg5.append(statistics.mean(ratioList[i - 5:i]))
        ratiosMovingAvg60.append(statistics.mean(ratioList[i - 60:i]))
        ratiosStd60.append(statistics.stdev(ratioList[i - 60:i]))
    for i in range(0, len(ratiosMovingAvg5)):
        if ratiosStd60[i] > 0:
            zscoreList.append((ratiosMovingAvg5[i] - ratiosMovingAvg60[i]) / ratiosStd60[i])
    if zscoreList[-1] > 1.5 or zscoreList[-1] < -1.5:
        df = pd.DataFrame({'y': list1, 'x': list2})
        result = coint_johansen(df, 0, 1)
        theta = result.eig[0]
        if theta > 0 or theta < 0:
            half_life = math.log(2) / theta
            finalSummaryList.append((half_life,hedgeRatio,item[0],item[1],item[2],item[3],item[4],item[5],zscoreList[-1]))

finalSummaryList.sort(key=itemgetter(0))
for item in finalSummaryList[0:1000]:
    print(item)

exit()


firstIndex = 4
secondIndex = 18
list1 = listClosePrices[firstIndex][0]
list2 = listClosePrices[secondIndex][0]
print(listClosePrices[firstIndex][1])
print(listClosePrices[secondIndex][1])
model = sm.OLS(list1,list2)
hedgeRatio = model.fit().params[0]
ratioList = []
for i in range(0,len(list1)):
    ratioList.append(list1[i] - hedgeRatio*list2[i])
adf = st.adfuller(ratioList)
print(adf)
print("Number of lookback days: " + str(len(ratioList)))
print("hedge ratio: " + str(hedgeRatio))
xpoints = range(0,len(ratioList))
plt.plot(xpoints,ratioList)
plt.axhline(statistics.mean(ratioList))
plt.show()
maxmin = []
for i in range(0,len(ratioList)):
    maxmin.append((i,ratioList[i]))
maxmin.sort(key=itemgetter(1))
for item in maxmin[:4]:
    print("portfolio value: " + str(item[1]))
    for i in range(0,10):
        if item[0] + i < len(list1):
            print(list1[item[0]+i] - hedgeRatio*list2[item[0]+i])

print("--- done with mins, now the maxes")
maxmin.sort(key = itemgetter(1),reverse=True)
for item in maxmin[:4]:
    print("portfolio value: " + str(item[1]))
    for i in range(0,10):
        if item[0] + i < len(list1):
            print(list1[item[0]+i] - hedgeRatio*list2[item[0]+i])
zlist = []
ratioListMean = statistics.mean(ratioList)
ratioListstdv = statistics.stdev(ratioList)
for item in ratioList:
    zlist.append((item-ratioListMean)/ratioListstdv)
plt.plot(xpoints,zlist)
plt.axhline(statistics.mean(zlist))
plt.axhline(1.0, color="red")
plt.axhline(-1.0, color="green")
plt.show()


exit()
ratiosMovingAvg5 = []
ratiosMovingAvg60 = []
ratiosStd60 = []
zscoreList = []

for i in range(60,len(ratioList)):
    ratiosMovingAvg5.append(statistics.mean(ratioList[i-5:i]))
    ratiosMovingAvg60.append(statistics.mean(ratioList[i-60:i]))
    ratiosStd60.append(statistics.stdev(ratioList[i-60:i]))

for i in range(0, len(ratiosMovingAvg5)):
    zscoreList.append((ratiosMovingAvg5[i]-ratiosMovingAvg60[i])/ratiosStd60[i])
xpoints = range(0,len(zscoreList))
plt.figure(figsize=(15,7))
plt.plot(xpoints,zscoreList)
plt.axhline(0, color='black')
plt.axhline(1.0, color='red', linestyle='--')
plt.axhline(-2.0, color='green', linestyle='--')
plt.show()


firstPriceList = listClosePrices[firstIndex][0]
secondPriceList = listClosePrices[secondIndex][0]
firstPriceList = firstPriceList[60:len(ratioList)]
secondPriceList = secondPriceList[60:len(ratioList)]

ratioList = ratioList[60:len(ratioList)]
minList = []
min = 0
for i in range(1,len(zscoreList)-1):
    if min == 0 and zscoreList[i] < zscoreList[i+1] and zscoreList[i] < zscoreList[i-1] and zscoreList[i] < -2:
        print(str(i))
        min = 1
        diffList = []
        tempRatioList = []
        j = i
        minList.append(i)
        # boll = abs(
        #     firstPriceList[i] - statistics.mean(firstPriceList[day - 19:day + 1])) / statistics.stdev(
        #     listClosePrices[i][0][day - 19:day + 1])
        while j < len(zscoreList) and zscoreList[j] < .5:
            diffList.append(round((firstPriceList[j]) - ratioList[i]*secondPriceList[j],2))
            tempRatioList.append(round(float(zscoreList[j]),2))
            j = j + 1
        print(diffList)
        print(tempRatioList)
    if min == 1 and zscoreList[i] > 0:
        min = 0
xpoints = range(0,len(firstPriceList))
plt.plot(xpoints,firstPriceList)
plt.plot(xpoints,secondPriceList)
for item in minList:
    plt.axvline(x=item, color='black')
plt.show()
# Y2 = pd.Series(np.random.normal(0, 1, 800), name='Y2') + 20
# Y3 = Y2.copy()
# Y3[0:100] = 30
# Y3[100:200] = 101
# Y3[200:300] = 30
# Y3[300:400] = 80
# Y3[400:500] = 30
# Y3[500:800] = 10000
#
# print( 'Correlation: ' + str(Y2.corr(Y3)))
# score, pvalue, _ = st.coint(Y2,Y3)
# print('Cointegration test p-value: ' + str(pvalue))
#
# ret1 = np.random.normal(1, 1, 100)
# ret2 = np.random.normal(2, 1, 100)
# s1 = pd.Series( np.cumsum(ret1), name='X2')
# s2 = pd.Series( np.cumsum(ret2), name='Y2')
#
# pd.concat([s1, s2], axis=1 ).plot(figsize=(15,7))
# plt.show()
#
# print( 'Correlation: ' + str(s1.corr(s2)))
# score, pvalue, _ = st.coint(s1,s2)
# print( 'Cointegration test p-value: ' + str(pvalue))