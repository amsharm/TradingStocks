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


totalCount = 0
zscoreRevertTotal = 0
adfCount = [0]*100
adfWinners = [0]*100
adfPct = [0]*100
negativeRatioAvg = [0]*100
negativeRatioTotal = [0]*100
negativeRatioCount = [0]*100
positiveRatioAvg = [0]*100
positiveRatioTotal = [0]*100
positiveRatioCount = [0]*100
winners10day = 0
winners20day = 0
winners30day = 0
overallRatioAvg = [-999]*100
totalNegativeStart = 0
negativeToPositiveDayList = [0]*100
positiveStartDailyAvg = [0]*100
positiveStartDailyCount = [0]*100
positiveStartDailyTotal = [0]*100
halfLife3Count = [0]*100
halfLife3Total = [0]*100
halfLife3Avg = [0]*100
halfLife6Count = [0]*50
halfLife6Total = [0]*50
halfLife6Avg = [0]*50
halfLife9Count = [0]*50
halfLife9Total = [0]*50
halfLife9Avg = [0]*50
summaryList = []
totalPositiveStart = 0
meanRevertTotal = [0]*100
meanRevertCount = [0]*100
meanRevertAvg = [0]*100
zscoreRateofChangeTotal = [0]*100
zscoreRateofChangeCount = [0]*100
zscoreRateofChangeAvg = [0]*100
zthreshold = 1
zturningPoint = [0]*10
zhalfcombinedTotal = [0] * 100
zhalfcombinedCount = [0] * 100
zhalfcombinedAvg = [0] * 100
zhalfcombinedTotal2 = [0] * 100
zhalfcombinedCount2 = [0] * 100
zhalfcombinedAvg2 = [0] * 100
midpointWinners10 = 0
midpointWinners20 = 0
midpointWinners30 = 0
adfLimit = -2.9

listFiles = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    listFiles.append(file)
print(len(listFiles))
for masterIndex in range(1,2):
    masterLength = 250*masterIndex
    secondLength = 250*(masterIndex-1)
    print("Master length: " + str(masterLength))
    print("Second length: " + str(secondLength))
    listClosePrices = []
    listVolumes = []
    for file in listFiles:
        tempList = []
        volumeList = []
        try:
            with open(file, "r") as inputfile:
                csvreader = csv.reader(inputfile)
                header = next(csvreader)
                for row in csvreader:
                    tempList.append(float(row[5]))
                    volumeList.append(float(row[6]))
            if len(tempList) > masterLength:
                listClosePrices.append((tempList[len(tempList)-masterLength:len(tempList)-secondLength],file.split("\\")[1].split(".")[0]))
                listVolumes.append(volumeList[len(tempList)-masterLength:len(tempList)-secondLength])
        except:
            print("blank: " +file)
    print("Number of stocks read: " + str(len(listClosePrices)))
    print("ADF limit: " + str(adfLimit))
    print("Z threshold is: " + str(zthreshold))
    for x in range(0,len(listClosePrices)-1):
        print(str(masterIndex) + " - " + str(x) + " - " + str(listClosePrices[x][1]))
        print(len(summaryList))

        print("Total crossings: " + str(totalCount))
        # if totalCount > 0:
        #     print(100*round(winners10day/totalCount,4))
        #     print(100*round(winners20day/totalCount,4))
        #     print(100*round(winners30day/totalCount,4))
        #     print(100*round(midpointWinners10 / totalCount, 4))
        #     print(100*round(midpointWinners20 / totalCount, 4))
        #     print(100*round(midpointWinners30 / totalCount, 4))
        # for i in range(0,100):
        #     if positiveRatioCount[i] > 0:
        #         positiveRatioAvg[i] = round(positiveRatioTotal[i]/positiveRatioCount[i],2)
        # for i in range(0,100):
        #     if zhalfcombinedCount[i] > 0:
        #         zhalfcombinedAvg[i] = round(zhalfcombinedTotal[i]/zhalfcombinedCount[i],2)
        # for i in range(0,100):
        #     if zhalfcombinedCount2[i] > 0:
        #         zhalfcombinedAvg2[i] = round(zhalfcombinedTotal2[i]/zhalfcombinedCount2[i],2)
        # for i in range(0,100):
        #     if negativeRatioCount[i] > 0:
        #         negativeRatioAvg[i] = round(negativeRatioTotal[i]/negativeRatioCount[i],2)
        # for i in range(0,100):
        #     if positiveStartDailyCount[i] > 0:
        #         positiveStartDailyAvg[i] = round(positiveStartDailyTotal[i]/positiveStartDailyCount[i],2)
        for i in range(0,100):
            if halfLife3Count[i] > 0:
                halfLife3Avg[i] = round(halfLife3Total[i]/halfLife3Count[i],2)
            # if halfLife6Count[i] > 0:
            #     halfLife6Avg[i] = round(halfLife6Total[i]/halfLife6Count[i],2)
            # if halfLife9Count[i] > 0:
            #     halfLife9Avg[i] = round(halfLife9Total[i]/halfLife9Count[i],2)
        # for i in range(0,100):
        #     if positivezscoreCount[i] > 0:
        #         positivezscoreAvg[i] = round(positivezscoreTotal[i]/positivezscoreCount[i],2)
        # for i in range(0,100):
        #     if negativezscoreCount[i] > 0:
        #         negativezscoreAvg[i] = round(negativezscoreTotal[i]/negativezscoreCount[i],2)
        # for i in range(0,100):
        #     if negativeRatioCount[i] + positiveRatioCount[i] > 0:
        #         overallRatioAvg[i] = round(((negativeRatioAvg[i]*negativeRatioCount[i]+positiveRatioCount[i]*positiveRatioAvg[i])/(negativeRatioCount[i]+positiveRatioCount[i])),2)
        # for i in range(0,100):
        #     if meanRevertCount[i] > 0:
        #         meanRevertAvg[i] = meanRevertTotal[i]/meanRevertCount[i]
        for i in range(0,100):
            if zscoreRateofChangeCount[i] > 0:
                zscoreRateofChangeAvg[i] = zscoreRateofChangeTotal[i]/zscoreRateofChangeCount[i]
        # print("----- Positive Ratio Returns -----")
        # for i in range(0, 100):
        #     if positiveRatioAvg[i] > 0:
        #         print(str(i) + " " + str(positiveRatioCount[i]) + " " + str(positiveRatioAvg[i]))
        # print("----- Combined - product - Half life and Z score change average days to return to half mean -----")
        # for i in range(0, 100):
        #     if zhalfcombinedAvg[i] > 0:
        #         print(str(i) + " " + str(zhalfcombinedCount[i]) + " " + str(zhalfcombinedAvg[i]))
        # print("----- Combined 2 - sum - Half life and Z score change average days to return to half mean -----")
        # for i in range(0, 100):
        #     if zhalfcombinedAvg2[i] > 0:
        #         print(str(i) + " " + str(zhalfcombinedCount2[i]) + " " + str(zhalfcombinedAvg2[i]))
        # print("----- Negative Ratio Returns -----")
        # for i in range(0, 100):
        #     if negativeRatioAvg[i] < 0:
        #         print(str(i) + " " + str(negativeRatioCount[i]) + " " + str(negativeRatioAvg[i]))
        # print("----- Overall Ratio Returns -----")
        # for i in range(0, 100):
        #     if overallRatioAvg[i]>-999:
        #         print(str(i) + " " + str(overallRatioAvg[i]))
        # print("----- Positive Start Daily Returns -----")
        # print(str(totalPositiveStart))
        # for i in range(0, 100):
        #     if positiveStartDailyAvg[i] > 0:
        #         print(str(i) + " " + str(positiveStartDailyAvg[i]))
        # print("----- Negative Start Number of Days to Become Positive  -----")
        # print(str(totalNegativeStart))
        # for i in range(0, 100):
        #     if totalNegativeStart > 0 and negativeToPositiveDayList[i] > 0:
        #         print(str(i) + " " + str(100*round(negativeToPositiveDayList[i]/totalNegativeStart,3)))
        # print("----- Mean reverting days for consecutive z score change  -----")
        # for i in range(0, 100):
        #     if meanRevertAvg[i] > 0:
        #         print(str(i) + " " + str(meanRevertCount[i]) + " " + str(meanRevertAvg[i]))
        print("----- Z score rate of change - numdays to revert to mean  -----")
        for i in range(0, 100):
            if zscoreRateofChangeAvg[i] > 0:
                print(str(i) + " " + str(zscoreRateofChangeCount[i]) + " " + str(zscoreRateofChangeAvg[i]))
        print("----- Half life Num days to revert to mean  -----")
        for i in range(0, 100):
            if halfLife3Avg[i] > 0:
                print(str(i) + " " + str(halfLife3Count[i]) + " " + str(halfLife3Avg[i]))
        # for i in range(0,10):
        #     if totalCount > 0:
        #         print(str(i) + " " + str(round(zturningPoint[i]/totalCount,4)*100))
        # for i in range(1,10):
        #     if totalCount > 0 and zturningPoint[i-1] > 0:
        #         print(str(i) + " " + str(round(zturningPoint[i]/zturningPoint[i-1],4)*100))
        # print("----- Half life 6 day average return  -----")
        # for i in range(0, 50):
        #     if halfLife6Avg[i] > 0:
        #         print(str(i) + " " + str(halfLife6Count[i]) + " " + str(halfLife6Avg[i]))
        # print("----- Half life 9 day average return  -----")
        # for i in range(0, 50):
        #     if halfLife9Avg[i] > 0:
        #         print(str(i) + " " + str(halfLife9Count[i]) + " " + str(halfLife9Avg[i]))
        # print("----- Positive Z Score Change -----")
        # for i in range(0, 100):
        #     if positivezscoreAvg[i] > 0:
        #         print(str(i) + " " + str(positivezscoreCount[i]) + " " + str(positivezscoreAvg[i]))
        # print("----- Negative Z Score Change-----")
        # for i in range(0, 100):
        #     if negativezscoreAvg[i] < 0:
        #         print(str(i) + " " + str(negativezscoreCount[i]) + " " + str(negativezscoreAvg[i]))

        #print("---------------------------------------")
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
            for i in range(60, len(ratioList)):
                ratiosMovingAvg5.append(statistics.mean(ratioList[i - 5:i]))
                ratiosMovingAvg60.append(statistics.mean(ratioList[i - 60:i]))
                ratiosStd60.append(statistics.stdev(ratioList[i - 60:i]))
            for i in range(0, len(ratiosMovingAvg5)):
                if ratiosStd60[i] > 0:
                    zscoreList.append((ratiosMovingAvg5[i] - ratiosMovingAvg60[i]) / ratiosStd60[i])
            currentCount = 0
            index = 9
            df = pd.DataFrame({'y': list1, 'x': list2})
            result = coint_johansen(df, 0, 1)
            theta = result.eig[0]
            half_life = math.log(2) / theta
            half_life = round(half_life)-6
            adfValue = adf[0]
            average = statistics.mean(ratioList)

            if adfValue < adfLimit and half_life > 0:
                while index < len(zscoreList) - 31:
                    index = index + 1
                    if zscoreList[index] > zthreshold and zscoreList[index] == max(zscoreList[index-10:index+3]):
                        index2 = index
                        while index2 < index+50 and index2 < len(zscoreList) and ratioList[index2+60] > average:
                            index2 = index2 + 1
                        zrateofchange = int(round((zscoreList[index] - zscoreList[index+3])/3,2)*100)
                        #if 0 < zrateofchange < 40:
                        if 0 < zrateofchange < 100:
                            #zrateofchange = 40 - zrateofchange
                            zscoreRateofChangeCount[zrateofchange] = zscoreRateofChangeCount[zrateofchange] + 1
                            zscoreRateofChangeTotal[zrateofchange] = zscoreRateofChangeTotal[zrateofchange] + index2-index
                            #combined = int(round(math.sqrt(half_life*zrateofchange)))
                            if 1==0:
                                 # zhalfcombinedCount[combined] = zhalfcombinedCount[combined] + 1
                                 # zhalfcombinedTotal[combined] = zhalfcombinedTotal[combined] + index2-index

                                currentCount = currentCount + 1

                                profit10 = False
                                profit20 = False
                                profit30 = False
                                profit10mid = False
                                profit20mid = False
                                profit30mid = False

                                for index2 in range(index,index+10):
                                    if ratioList[index2 + 60] < average:
                                        profit10 = True
                                for index2 in range(index,index+20):
                                    if ratioList[index2 + 60] < average:
                                        profit20 = True
                                for index2 in range(index,index+30):
                                    if ratioList[index2 + 60] < average:
                                        profit30 = True
                                for index2 in range(index,index+10):
                                    if ratioList[index2 + 60] < (ratioList[index+60]+average)/2:
                                        profit10mid = True
                                for index2 in range(index,index+20):
                                    if ratioList[index2 + 60] < (ratioList[index+60]+average)/2:
                                        profit20mid = True
                                for index2 in range(index,index+30):
                                    if ratioList[index2 + 60] < (ratioList[index+60]+average)/2:
                                        profit30mid = True
                                if profit10 == True:
                                    winners10day = winners10day + 1
                                if profit20 == True:
                                    winners20day = winners20day + 1
                                if profit30 == True:
                                    winners30day = winners30day + 1
                                if profit10mid == True:
                                    midpointWinners10 = midpointWinners10 + 1
                                if profit20mid == True:
                                    midpointWinners20 = midpointWinners20 + 1
                                if profit30mid == True:
                                    midpointWinners30 = midpointWinners30 + 1

                        # meanRevertCount[0] = meanRevertCount[0] + 1
                        # meanRevertTotal[0] = meanRevertTotal[0] + index2-index
                        if 0 < half_life < 100:
                            halfLife3Count[half_life] = halfLife3Count[half_life] + 1
                            halfLife3Total[half_life] = halfLife3Total[half_life] + index2-index
                        # index3 = index + 1
                        # counter = 1
                        # while index3 < len(zscoreList) and zscoreList[index3] < zscoreList[index3-1] and counter < 100:
                        #     meanRevertCount[counter] = meanRevertCount[counter] + 1
                        #     meanRevertTotal[counter] = meanRevertTotal[counter] + index2-index
                        #     index3 = index3 + 1
                        #     counter = counter + 1
                        # zrateofchange = int(round((zscoreList[index] - zscoreList[index+3])/3,2)*100)
                        # if 0 < zrateofchange < 36:
                        #     zrateofchange = 36 - zrateofchange
                        #     # zscoreRateofChangeCount[zrateofchange] = zscoreRateofChangeCount[zrateofchange] + 1
                        #     # zscoreRateofChangeTotal[zrateofchange] = zscoreRateofChangeTotal[zrateofchange] + index2-index
                        #     combined = int(round(math.sqrt(half_life*zrateofchange)))
                        #     combined2 = half_life + zrateofchange
                        #     if 0 <= combined < 50:
                        #         zhalfcombinedCount[combined] = zhalfcombinedCount[combined] + 1
                        #         zhalfcombinedTotal[combined] = zhalfcombinedTotal[combined] + index2-index
                        #     if 0 <= combined2 < 100:
                        #         zhalfcombinedCount2[combined2] = zhalfcombinedCount2[combined2] + 1
                        #         zhalfcombinedTotal2[combined2] = zhalfcombinedTotal2[combined2] + index2-index
                        while zscoreList[index] > zthreshold and index < len(zscoreList) - 11:
                            index = index + 1
                    elif zscoreList[index] < -1*zthreshold and zscoreList[index] == min(zscoreList[index-10:index+3]):
                        index2 = index
                        while index2 < index + 50 and index2 < len(zscoreList) and ratioList[index2 + 60] < average:
                            index2 = index2 + 1

                        if 0 < half_life < 100:
                            halfLife3Count[half_life] = halfLife3Count[half_life] + 1
                            halfLife3Total[half_life] = halfLife3Total[half_life] + index2-index
                        zrateofchange = int(round((zscoreList[index + 3] - zscoreList[index]) / 3, 2) * 100)
                        #if 0 < zrateofchange < 40:
                        if 0 < zrateofchange < 100:
                            zscoreRateofChangeCount[zrateofchange] = zscoreRateofChangeCount[zrateofchange] + 1
                            zscoreRateofChangeTotal[zrateofchange] = zscoreRateofChangeTotal[zrateofchange] + index2 - index
                            #zrateofchange = 40 - zrateofchange
                            #combined = int(round(math.sqrt(half_life * zrateofchange)))
                            #if 0 <= combined < 16:
                            if 0==1:
                                 # zhalfcombinedCount[combined] = zhalfcombinedCount[combined] + 1
                                 # zhalfcombinedTotal[combined] = zhalfcombinedTotal[combined] + index2 - index
                        #if 0 < zrateofchange < 36:
                        #     zrateofchange = 36 - zrateofchange
                        #     combined = int(round(math.sqrt(half_life * zrateofchange)))
                        #     if combined < 15:
                                currentCount = currentCount + 1
                        # index2 = index + 1
                        # while zscoreList[index2 + 1] > zscoreList[index2] and (index2 - index < 10):
                        #     zturningPoint[index2 - index] = zturningPoint[index2 - index] + 1
                        #     index2 = index2 + 1
                                profit10 = False
                                profit20 = False
                                profit30 = False
                                profit10mid = False
                                profit20mid = False
                                profit30mid = False
                                for index2 in range(index, index + 10):
                                    if ratioList[index2 + 60] > average:
                                        profit10 = True
                                for index2 in range(index, index + 20):
                                    if ratioList[index2 + 60] > average:
                                        profit20 = True
                                for index2 in range(index, index + 30):
                                    if ratioList[index2 + 60] > average:
                                        profit30 = True
                                for index2 in range(index,index+10):
                                    if ratioList[index2 + 60] > (ratioList[index+60]+average)/2:
                                        profit10mid = True
                                for index2 in range(index,index+20):
                                    if ratioList[index2 + 60] > (ratioList[index+60]+average)/2:
                                        profit20mid = True
                                for index2 in range(index,index+30):
                                    if ratioList[index2 + 60] > (ratioList[index+60]+average)/2:
                                        profit30mid = True
                                if profit10 == True:
                                    winners10day = winners10day + 1
                                if profit20 == True:
                                    winners20day = winners20day + 1
                                if profit30 == True:
                                    winners30day = winners30day + 1
                                if profit10mid == True:
                                    midpointWinners10 = midpointWinners10 + 1
                                if profit20mid == True:
                                    midpointWinners20 = midpointWinners20 + 1
                                if profit30mid == True:
                                    midpointWinners30 = midpointWinners30 + 1
                        # meanRevertCount[0] = meanRevertCount[0] + 1
                        # meanRevertTotal[0] = meanRevertTotal[0] + index2 - index
                        # index3 = index + 1
                        # counter = 1
                        # while index3 < len(zscoreList) and zscoreList[index3] > zscoreList[index3 - 1] and counter < 100:
                        #     meanRevertCount[counter] = meanRevertCount[counter] + 1
                        #     meanRevertTotal[counter] = meanRevertTotal[counter] + index2 - index
                        #     index3 = index3 + 1
                        #     counter = counter + 1
                        # zrateofchange = int(round((zscoreList[index + 3] - zscoreList[index]) / 3, 2) * 100)
                        # if 0 < zrateofchange < 36:
                        #     zrateofchange = 36 - zrateofchange
                        #     combined = int(round(math.sqrt(half_life * zrateofchange)))
                        #     combined2 = half_life + zrateofchange
                        #     if 0 <= combined < 50:
                        #         zhalfcombinedCount[combined] = zhalfcombinedCount[combined] + 1
                        #         zhalfcombinedTotal[combined] = zhalfcombinedTotal[combined] + index2 - index
                        #     if 0 <= combined2 < 100:
                        #         zhalfcombinedCount2[combined2] = zhalfcombinedCount2[combined2] + 1
                        #         zhalfcombinedTotal2[combined2] = zhalfcombinedTotal2[combined2] + index2 - index
                        #     # zscoreRateofChangeCount[zrateofchange] = zscoreRateofChangeCount[zrateofchange] + 1
                        #     # zscoreRateofChangeTotal[zrateofchange] = zscoreRateofChangeTotal[zrateofchange] + index2 - index
                        while zscoreList[index] < -1*zthreshold and index < len(zscoreList) - 11:
                            index = index + 1
            totalCount = totalCount + currentCount
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

exit()

# profit10 = False
#                             profit20 = False
#                             profit30 = False
#                             for index2 in range(index,index+10):
#                                 if ratioList[index2 + 60] < ratioList[index + 60]:
#                                     profit10 = True
#                             for index2 in range(index,index+20):
#                                 if ratioList[index2 + 60] < ratioList[index + 60]:
#                                     profit20 = True
#                             for index2 in range(index,index+30):
#                                 if ratioList[index2 + 60] < ratioList[index + 60]:
#                                     profit30 = True
#                             if profit10 == True:
#                                 winners10day = winners10day + 1
#                             if profit20 == True:
#                                 winners20day = winners20day + 1
#                             if profit30 == True:
#                                 winners30day = winners30day + 1

# boll1 = abs(list1[index + 60] - statistics.mean(
                        #     list1[index + 41:index + 61])) / statistics.stdev(
                        #     list1[index + 41:index + 61])
                        # boll2 = abs(list2[index + 60] - statistics.mean(
                        #     list2[index + 41:index + 61])) / statistics.stdev(
                        #     list2[index + 41:index + 61])
                        # boll = int(round((boll2 + boll1), 1) * 10)
# if 0< half_life < 50:
                            #     curRatioDiff3 = (ratioList[index + 63] - ratioList[index + 60])/3
                            #     curRatioDiff6 = (ratioList[index + 66] - ratioList[index + 60])/6
                            #     curRatioDiff9 = (ratioList[index + 69] - ratioList[index + 60])/9
                            #     halfLife3Count[half_life] = halfLife3Count[half_life] + 1
                            #     halfLife6Count[half_life] = halfLife6Count[half_life] + 1
                            #     halfLife9Count[half_life] = halfLife9Count[half_life] + 1
                            #     halfLife3Total[half_life] = halfLife3Total[half_life] + curRatioDiff3
                            #     halfLife6Total[half_life] = halfLife6Total[half_life] + curRatioDiff6
                            #     halfLife9Total[half_life] = halfLife9Total[half_life] + curRatioDiff9
totalCount = 0
finalSummaryList = []
# print(index)
#                                     print(y)
#                                     print(listClosePrices[y][1])
#                                     xpoints = range(0, len(zscoreList))
#                                     plt.plot(xpoints, zscoreList)
#                                     plt.show()
#                                     xpoints = range(0,len(ratioList))
#                                     plt.plot(xpoints,ratioList)
#                                     plt.axhline(average, color="red")
#                                     plt.show()
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

