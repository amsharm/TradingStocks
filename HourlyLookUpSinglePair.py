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


    firstTicker = equityA
    secondTicker = equityB
    listFiles = []
    listClosePrices = []
    for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Hourly Data/*.csv"):
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
                        try:
                            tempList.append(float(row[4]))
                        except:
                            pass

                    listClosePrices.append((tempList[len(tempList)-numDays:len(tempList)],file.split("\\")[1].split(".")[0]))

            except:
                print("blank: " + file + str(row[5]))


    print("Number of stocks read: " + str(len(listClosePrices)))

    for x in range(0,len(listClosePrices)):
        if listClosePrices[x][1] == firstTicker:
            firstIndex = x
        if listClosePrices[x][1] == secondTicker:
            secondIndex = x
    print(firstIndex)
    print(secondIndex)
    list1 = listClosePrices[firstIndex][0]
    list2 = listClosePrices[secondIndex][0]
    print(listClosePrices[firstIndex][1])
    print(listClosePrices[secondIndex][1])


    #list1 = list1[1200:1500]
    #list2 = list2[1200:1500]
    model = sm.OLS(list1, list2)
    hedgeRatio = model.fit().params[0]
    if hedgeratio !=0:
        hedgeRatio = hedgeratio
    #hedgeRatio = .4435
    print("Hedge ratio: "+str(hedgeRatio))
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
    plt.figure(figsize=(15, 7))
    plt.plot(xpoints, ratioList)
    plt.axhline(0, color="red")
    plt.axhline(statistics.mean(ratioList),color="green")
    print("Last price for: "+str(firstTicker)+" "+str(list1[-1]))
    print("Last price for: "+str(secondTicker)+" "+str(list2[-1]))
    print("Second to last price for: "+str(firstTicker)+" "+str(list1[-2]))
    print("Second to last price for: "+str(secondTicker)+" "+str(list2[-2]))
    print("Last ratio value: "+str(ratioList[-1]))
    print("Second to last ratio value: "+str(ratioList[-2]))
    plt.show()
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
lookUpPair("BWA","WMB",500,0)
exit()
file = "C:/Users/17132/Desktop/Hourly Optimal Pairs/Hourly - Aug 31.txt"
#file = "C:/Users/17132/Desktop/Hourly Optimal Pairs/Hourly - Aug 31.txt"
#file = "C:/Users/17132/Desktop/Long Term Cointegrated Stocks/Aug 25.txt"

with open(file, "r") as inputfile:
    while True:
        line = inputfile.readline()
        equityA = line.split(",")[0].replace("'","").replace(")","").replace("(","").strip()
        equityB = line.split(",")[1].replace("'","").replace(")","").replace("(","").strip()
        print(equityA)
        print(equityB)
        #outList.append((distance,halflife,equityA,equityB))
        try:
            lookUpPair(equityA,equityB,250,0)
            #lookUpPair(equityA, equityB, 250, 0)
        except:
            pass

