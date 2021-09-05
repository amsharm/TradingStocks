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
from statsmodels import regression
from scipy import stats

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

listFiles = []
listClosePrices = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    listFiles.append(file)
masterLength = 250
print(len(listFiles))
listVolumes = []
for file in listFiles:
    tempList = []
    volumeList = []
    with open(file, "r") as inputfile:
        csvreader = csv.reader(inputfile)
        header = next(csvreader)
        for row in csvreader:
            try:
                tempList.append(float(row[5]))
                volumeList.append(float(row[6]))
            except:
                print("blank: "+str(row[5]))
    if len(tempList) > masterLength:
        listClosePrices.append((tempList[len(tempList)-masterLength:len(tempList)],file.split("\\")[1].split(".")[0]))
        listVolumes.append(volumeList[len(tempList)-masterLength:len(tempList)])
# listClosePrices.append((btcPrices[26000:28003],"BTC"))
# listClosePrices.append((ethPrices[26000:28003],"ETH"))
print("Number of stocks read: " + str(len(listClosePrices)))


summaryList = []
print(len(listClosePrices[0][0]))
totalCount = 0
totalWinners = 0
lowADFCount = 0
lowADFWinners = 0
halfLifeCount = [0]*1000
halfLifeWinners = [0]*1000
halfLifePct = [0]*1000
bollingerCount = [0]*100
bollingerWinners = [0]*100
bollingerPct = [0]*100
lowADF31Count = 0
lowADF31Winners = 0
lowADF32Count = 0
lowADF32Winners = 0
lowADF33Winners = 0
lowADF33Count = 0
lowADF27Count = 0
lowADF27Winners = 0
lowADF29Count = 0
lowADF29Winners = 0
exceptionList = []
lowADF28Count = 0
lowADF28Winners = 0
betaRatioCount = [0]*100
betaRatioWinners = [0]*100
betaRatioPct = [0]*100
volumeRCount = [0]*1000
volumeRWinners = [0]*1000
volumeRPct = [0]*1000
zscoreRevertTotal = 0
adfCount = [0]*100
adfWinners = [0]*100
adfPct = [0]*100

for x in range(0,len(listClosePrices)-1):
    print(str(x) + " - " + str(listClosePrices[x][1]))
    print("Total crossings: " + str(totalCount))
    if totalCount > 0:
        print(round(totalWinners/totalCount,4))
        print(round(zscoreRevertTotal/totalCount,4))
    print("Total <2.7 ADF count: " + str(lowADF27Count))
    if lowADF27Count > 0:
        print(round(lowADF27Winners / lowADF27Count, 4))
    print("Total <2.8 ADF count: " + str(lowADF28Count))
    if lowADF28Count > 0:
        print(round(lowADF28Winners / lowADF28Count, 4))
    print("Total <2.9 ADF count: " + str(lowADF29Count))
    if lowADF29Count > 0:
        print(round(lowADF29Winners / lowADF29Count, 4))
    print("Total <3 ADF count: " + str(lowADFCount))
    if lowADFCount > 0:
        print(round(lowADFWinners/lowADFCount,4))
    print("Total <3.1 ADF count: " + str(lowADF31Count))
    if lowADF31Count > 0:
        print(round(lowADF31Winners/lowADF31Count,4))
    print("Total <3.2 ADF count: " + str(lowADF32Count))
    if lowADF32Count > 0:
        print(round(lowADF32Winners/lowADF32Count,4))
    print("Total <3.3 ADF count: " + str(lowADF33Count))
    if lowADF33Count > 0:
        print(round(lowADF33Winners/lowADF33Count,4))

    for i in range(0,100):
        if adfCount[i] > 100:
            adfPct[i] = round(adfWinners[i]/adfCount[i],2)
    for i in range(0,1000):
        if halfLifeCount[i] > 0:
            halfLifePct[i] = round(halfLifeWinners[i]/halfLifeCount[i],2)
    for i in range(0,100):
        if bollingerCount[i] > 0:
            bollingerPct[i] = round(bollingerWinners[i]/bollingerCount[i],2)
    for i in range(0,100):
        if betaRatioCount[i] > 0:
            betaRatioPct[i] = round(betaRatioWinners[i]/betaRatioCount[i],2)
    for i in range(0,1000):
        if volumeRCount[i] > 100:
            volumeRPct[i] = round(volumeRWinners[i]/volumeRCount[i],2)
    print("----- ADF Value -----")
    for i in range(0, 100):
        if adfPct[i] > 0:
            print(str(i) + " - " + str(adfCount[i]) + " - " + str(adfPct[i]))
    print("----- Half Life -----")
    for i in range(0,1000):
        if halfLifePct[i] > 0:
            print(str(i)+" - " + str(halfLifeCount[i]) + " - " + str(halfLifePct[i]))
    print("----- Bollinger Score -----")
    for i in range(0,100):
        if bollingerPct[i] > 0:
            print(str(i)+" - " + str(bollingerCount[i]) + " - " + str(bollingerPct[i]))
    print("----- Beta Ratio -----")
    for i in range(0,100):
        if betaRatioPct[i] > 0:
            print(str(i)+" - " + str(betaRatioCount[i]) + " - " + str(betaRatioPct[i]))
    print("----- Volume Ratio -----")
    for i in range(0, 1000):
        if volumeRPct[i] > 0:
            print(str(i) + " - " + str(volumeRCount[i]) + " - " + str(volumeRPct[i]))
    for item in exceptionList[0:20]:
        print(item)
    print("---------------------------------------")
    for y in range(x+1,len(listClosePrices)):
        list1 = listClosePrices[x][0]
        list2 = listClosePrices[y][0]
        model = sm.OLS(list1,list2)
        hedgeRatio = model.fit().params[0]
        ratioList = []
        for i in range(0, len(list1)):
            ratioList.append(list1[i] - hedgeRatio * list2[i])
        adf = st.adfuller(ratioList)
        ratiosMovingAvg5 = []
        ratiosMovingAvg60 = []
        ratiosStd60 = []
        zscoreList = []
        # length of ratiolist is 500
        # length of zscorelist is 440
        for i in range(60, len(ratioList)):
            ratiosMovingAvg5.append(statistics.mean(ratioList[i - 5:i]))
            ratiosMovingAvg60.append(statistics.mean(ratioList[i - 60:i]))
            ratiosStd60.append(statistics.stdev(ratioList[i - 60:i]))
        for i in range(0, len(ratiosMovingAvg5)):
            if ratiosStd60[i] > 0:
                zscoreList.append((ratiosMovingAvg5[i] - ratiosMovingAvg60[i]) / ratiosStd60[i])
        currentCount = 0
        currentWinners = 0
        zscoreRevertCount = 0
        index = 10
        adfValue = adf[0]
        if adfValue > 0:
            adfValue = 0
        #adfValue = abs(adfValue)
        #adfValue = int(round(adfValue,1)*10)
        while index < len(zscoreList) - 11 and adfValue < -2.9:
            index = index + 1
            if zscoreList[index] > 2 and zscoreList[index] == max(zscoreList[index-10:index+10]):
                profit = False
                zscoreRevert = False
                for index2 in range(index,index+10):
                    if ratioList[index2+60] < ratioList[index+60]:
                        profit = True
                    if zscoreList[index2] < 0:
                        zscoreRevert = True
                tempzlist = []
                for item in zscoreList[index:index+10]:
                    tempzlist.append(round(item,2))
                print(tempzlist)
                currentCount = currentCount + 1
                if profit == True:
                    currentWinners = currentWinners + 1
                if zscoreRevert == True:
                    zscoreRevertCount = zscoreRevertCount + 1
                # boll1 = abs(listClosePrices[x][0][index+60] - statistics.mean(
                #     listClosePrices[x][0][index+41:index + 61])) / statistics.stdev(
                #     listClosePrices[x][0][index+41:index + 61])
                # boll2 = abs(listClosePrices[y][0][index + 60] - statistics.mean(
                #     listClosePrices[y][0][index + 41:index + 61])) / statistics.stdev(
                #     listClosePrices[y][0][index + 41:index + 61])
                # boll = int(round((boll2 + boll1),1)*10)
                # if 0 < boll < 100:
                #     bollingerCount[boll] = bollingerCount[boll] + 1
                #     if profit == True:
                #         bollingerWinners[boll] = bollingerWinners[boll] + 1
                # volumeRatio = statistics.mean(listVolumes[x][index+58:index+61])/statistics.mean(listVolumes[x][index+41:index+61]) + statistics.mean(listVolumes[y][index + 58:index + 61]) / statistics.mean(
                #     listVolumes[y][index + 41:index + 61])
                # volumeRatio = int(round(volumeRatio,2)*100)
                # if 0 < volumeRatio < 1000:
                #     volumeRCount[volumeRatio] = volumeRCount[volumeRatio] + 1
                #     if profit == True:
                #         volumeRWinners[volumeRatio] = volumeRWinners[volumeRatio] + 1
                # if 0 < adfValue < 100:
                #     adfCount[adfValue] = adfCount[adfValue] + 1
                #     if profit == True:
                #         adfWinners[adfValue] = adfWinners[adfValue] + 1
                while zscoreList[index] > 2 and index < len(zscoreList) - 11:
                    index = index + 1
            elif zscoreList[index] < -2 and zscoreList[index] == min(zscoreList[index-10:index+10]):
                profit = False
                zscoreRevert = False
                for index2 in range(index,index+10):
                    if ratioList[index2+60] > ratioList[index+60]:
                        profit = True
                    if zscoreList[index2] > 0:
                        zscoreRevert = True
                currentCount = currentCount + 1
                tempzlist = []
                for item in zscoreList[index:index + 10]:
                    tempzlist.append(round(item, 2))
                print(tempzlist)
                if profit == True:
                    currentWinners = currentWinners + 1
                if zscoreRevert == True:
                    zscoreRevertCount = zscoreRevertCount + 1
                # boll1 = abs(listClosePrices[x][0][index + 60] - statistics.mean(
                #     listClosePrices[x][0][index + 41:index + 61])) / statistics.stdev(
                #     listClosePrices[x][0][index + 41:index + 61])
                # boll2 = abs(listClosePrices[y][0][index + 60] - statistics.mean(
                #     listClosePrices[y][0][index + 41:index + 61])) / statistics.stdev(
                #     listClosePrices[y][0][index + 41:index + 61])
                # boll = int(round((boll2 + boll1), 1) * 10)
                # if 0 < boll < 100:
                #     bollingerCount[boll] = bollingerCount[boll] + 1
                #     if profit == True:
                #         bollingerWinners[boll] = bollingerWinners[boll] + 1
                # volumeRatio = statistics.mean(listVolumes[x][index + 58:index + 61]) / statistics.mean(
                #     listVolumes[x][index + 41:index + 61]) + statistics.mean(
                #     listVolumes[y][index + 58:index + 61]) / statistics.mean(
                #     listVolumes[y][index + 41:index + 61])
                # volumeRatio = int(round(volumeRatio, 2) * 100)
                # if 0 < volumeRatio < 1000:
                #     volumeRCount[volumeRatio] = volumeRCount[volumeRatio] + 1
                #     if profit == True:
                #         volumeRWinners[volumeRatio] = volumeRWinners[volumeRatio] + 1
                # if 0 < adfValue < 100:
                #     adfCount[adfValue] = adfCount[adfValue] + 1
                #     if profit == True:
                #         adfWinners[adfValue] = adfWinners[adfValue] + 1
                while zscoreList[index] < -2 and index < len(zscoreList) - 11:
                    index = index + 1
        totalCount = totalCount + currentCount
        totalWinners = totalWinners + currentWinners
        zscoreRevertTotal = zscoreRevertTotal + zscoreRevertCount
        # if adf[0] < -2.8:
        #     lowADF28Count = lowADF28Count + currentCount
        #     lowADF28Winners = lowADF28Winners + currentWinners
        # if adf[0] < -2.9:
        #     lowADF29Count = lowADF29Count + currentCount
        #     lowADF29Winners = lowADF29Winners + currentWinners
        # if adf[0] < -3:
        #     lowADFCount = lowADFCount + currentCount
        #     lowADFWinners = lowADFWinners + currentWinners
        # if adf[0] < -3.1:
        #     lowADF31Count = lowADF31Count + currentCount
        #     lowADF31Winners = lowADF31Winners + currentWinners
        # if adf[0] < -3.2:
        #     lowADF32Count = lowADF32Count + currentCount
        #     lowADF32Winners = lowADF32Winners + currentWinners
        # if adf[0] < -3.3:
        #     lowADF33Count = lowADF33Count + currentCount
        #     lowADF33Winners = lowADF33Winners + currentWinners
        # if adf[0] < -2.7:
        #     lowADF27Count = lowADF27Count + currentCount
        #     lowADF27Winners = lowADF27Winners + currentWinners
        #     if currentCount > currentWinners:
        #         exceptionList.append((x,y))
        # if betaList[x] > 0 and betaList[y] > 0:
        #     betaRatio = int(round(max(betaList[x],betaList[y])/min(betaList[x],betaList[y]),1)*10)
        #     if 0 < betaRatio < 100:
        #         betaRatioCount[betaRatio] = betaRatioCount[betaRatio] + currentCount
        #         betaRatioWinners[betaRatio] = betaRatioWinners[betaRatio] + currentWinners
        # df = pd.DataFrame({'y': list1, 'x': list2})
        # result = coint_johansen(df, 0, 1)
        # theta = result.eig[0]
        # if theta > 0 or theta < 0:
        #     half_life = math.log(2) / theta
        #     half_life = round(half_life)
        #     halfLifeCount[half_life] = halfLifeCount[half_life] + currentCount
        #     halfLifeWinners[half_life] = halfLifeWinners[half_life] + currentWinners

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

