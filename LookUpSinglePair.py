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

def lookUpPair(equityA, equityB, numDays, hedgeratio):
    listDates = GetTradingDates.getDates(numDays)
    listDates.reverse()
    #print("Number of days: " + str(numDays))

    #print(len(listDates))
    # btcPrices = []
    # ethPrices = []
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

    firstTicker = equityA
    secondTicker = equityB
    listFiles = []
    listClosePrices = []
    for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
        listFiles.append(file)
    for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
        listFiles.append(file)
    tempListPrices = []
    #print(len(listFiles))
    for file in listFiles:
        tempList = []
        if firstTicker == file.split("\\")[1].split(".")[0] or secondTicker == file.split("\\")[1].split(".")[0]:
            try:
                with open(file, "r") as inputfile:
                    csvreader = csv.reader(inputfile)
                    header = next(csvreader)
                    for row in csvreader:
                        tempList.append((row[0],float(row[5]),file.split("\\")[1].split(".")[0]))
                    tempList.reverse()
                    tempListPrices.append(tempList)

            except:
                print("blank: " + file + str(row[5]))
        # if len(tempList) > masterLength:
        #     listClosePrices.append((tempList[len(tempList)-masterLength:len(tempList)],file.split("\\")[1].split(".")[0]))
    # listClosePrices.append((btcPrices[26000:28003],"BTC"))
    # listClosePrices.append((ethPrices[26000:28003],"ETH"))
    # print(len(tempListPrices))
    # Check for duplicate dates
    for item in tempListPrices:
        tempdates = []
        for x in item:
            tempdates.append(x[0])
        if len(tempdates) != len(set(tempdates)):
            print("duplicates in " + str(item[2]))
            exit()
    # Extract each closing price for corresponding date
    #print("Extracting dates")
    #print("Number of dates: "+str(len(listDates)))
    counter = 0
    for item in tempListPrices:
        listPrices = []
        for date in listDates:
            counter = counter + 1
            found = False
            index = 0
            while found is False and index < len(listDates):
                if str(item[index][0]) == str(date):
                    listPrices.append(item[index][1])
                    found = True
                index = index + 1
            if found is False and len(listPrices) > 0:
                #print(date)
                listPrices.append(listPrices[-1])
        #print(len(listPrices))
        if len(listPrices) == numDays:
            listClosePrices.append((listPrices,item[2][2]))
    #print("-----------------")


    #print("Number of stocks read: " + str(len(listClosePrices)))
    summaryList = []
    #print(len(listClosePrices[0][0]))

    finalSummaryList = []


    for x in range(0,len(listClosePrices)):
        if listClosePrices[x][1] == firstTicker:
            firstIndex = x
        if listClosePrices[x][1] == secondTicker:
            secondIndex = x
    #print(firstIndex)
    #print(secondIndex)
    list1 = listClosePrices[firstIndex][0]
    list2 = listClosePrices[secondIndex][0]
    #print(listClosePrices[firstIndex][1])
    #print(listClosePrices[secondIndex][1])
    #list1 = list1[1200:1500]
    #list2 = list2[1200:1500]
    model = sm.OLS(list1, list2)
    hedgeRatio = model.fit().params[0]
    if hedgeratio !=0:
        hedgeRatio = hedgeratio
    #hedgeRatio = .4435
    #print("Hedge ratio: "+str(hedgeRatio))
    ratioList = []
    for i in range(0, len(list1)):
        ratioList.append(list1[i] - hedgeRatio * list2[i])
    adf = st.adfuller(ratioList)
    df = pd.DataFrame({'y': list1, 'x': list2})
    result = coint_johansen(df, 0, 1)
    theta = result.eig[0]
    half_life = math.log(2) / theta
    half_life = round(half_life) - 6
    print("ADF: " + str(adf[0]))
    print("Half-life: " + str(half_life))
    xpoints = range(0, len(ratioList))
    plt.figure(figsize=(14, 6))
    plt.plot(xpoints, ratioList)
    plt.axhline(0, color="red")
    plt.axhline(statistics.mean(ratioList),color="green")
    # print("Last price for: "+str(firstTicker)+" "+str(list1[-1]))
    # print("Last price for: "+str(secondTicker)+" "+str(list2[-1]))
    # print("Second to last price for: "+str(firstTicker)+" "+str(list1[-2]))
    # print("Second to last price for: "+str(secondTicker)+" "+str(list2[-2]))
    # print("Last ratio value: "+str(ratioList[-1]))
    # print("Second to last ratio value: "+str(ratioList[-2]))
    plt.show()
    return adf[0]
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
    # print(zscoreList[-1])
    # print(zscoreList[-2])
    # print(zscoreList[-3])
    #if zscoreList[-1] > 2 or zscoreList[-1] < -2:
    if 1==1:
        df = pd.DataFrame({'y': list1, 'x': list2})
        result = coint_johansen(df[len(list1)-150:], 0, 1)
        theta = result.eig[0]
        if theta > 0 or theta < 0:
            half_life = math.log(2) / theta
            #finalSummaryList.append((half_life,hedgeRatio,item[0],item[1],item[2],item[3],item[4],item[5],zscoreList[-1]))
        # xpoints = range(0, len(zscoreList))
        # plt.figure(figsize=(15, 7))
        # plt.plot(xpoints, zscoreList)
        # plt.axhline(0, color='black')
        # plt.axhline(2.0, color='red', linestyle='--')
        # plt.axhline(-2.0, color='green', linestyle='--')
        # plt.show()
    #
# finalSummaryList.sort(key=itemgetter(0))
# for item in finalSummaryList[0:1000]:
#     print(item)


#
lookUpPair("HBAN","MAR",250,0)
exit()
file = "C:/Users/17132/Desktop/Daily Optimal Pairs/Sep 4.txt"
# file = "C:/Users/17132/Desktop/Test/test4.txt"
#file = "C:/Users/17132/Desktop/Long Term Cointegrated Stocks/Aug 25.txt"
potentialList = []
with open(file, "r") as inputfile:
    lines = inputfile.readlines()
    for line in lines:
        if line.__contains__("Possibility"):
            equityA = line.split(",")[0].replace("'","").replace(")","").replace("(","").strip()
            equityB = line.split(",")[1].replace("'","").replace(")","").replace("(","").strip()
            potential = line.split(",")[5].replace("'","").replace(")","").replace("(","").strip()
            potentialList.append((equityA,equityB,potential))
            #outList.append((distance,halflife,equityA,equityB))
            adfList = []
            print(equityA)
            print(equityB)
            try:
                adfList.append(lookUpPair(equityA,equityB,250,0))
                # adfList.append(lookUpPair(equityA, equityB, 500, 0))
                # adfList.append(lookUpPair(equityA, equityB, 750, 0))
                # adfList.append(lookUpPair(equityA, equityB, 1000, 0))
                # for item in adfList:
                #     print(item)
                # print("------------------------------------------------------------------")
                #lookUpPair(equityA, equityB, 250, 0)
            except:
                pass
potentialList.sort(key=itemgetter(2),reverse=True)
for item in potentialList:
    print(item)

