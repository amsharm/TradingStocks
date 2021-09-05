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
import GetTradingDates


totalCount = 0
zscoreRevertTotal = 0
adfCount = [0]*100
adfWinners = [0]*100
adfPct = [0]*100
winners10day = 0
winners20day = 0
winners30day = 0
overallRatioAvg = [-999]*100
totalNegativeStart = 0
negativeToPositiveDayList = [0]*100
beta10Winners = [0]*300
beta20Winners = [0]*300
beta30Winners = [0]*300
beta10MidWinners = [0]*300
beta20MidWinners = [0]*300
beta30MidWinners = [0]*300
betaCount = [0]*300
summaryList = []
totalPositiveStart = 0
zthreshold = 1.5
zturningPoint = [0]*10
midpointWinners10 = 0
midpointWinners20 = 0
midpointWinners30 = 0
tempList = []
adfLimit = -2.9

numDays = 1000
listDates = GetTradingDates.getDates(numDays)
listDates.reverse()

betaList = []
file = "C:/Users/17132/Desktop/Beta Coefficients.txt"
with open(file, "r") as inputfile:
    try:
        while 1==1:
            line = inputfile.readline()
            line = line.replace("'","").replace("(","").replace(")","")
            betaList.append((line.split(",")[0].strip(),line.split(",")[1].strip()))
    except:
        pass

listFiles = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    listFiles.append(file)
print(len(listFiles))

tempListPrices = []
listClosePrices = []
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
    except:
        print("blank: " + file)

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
        betaScore = -999
        ticker = item[2][2]
        for item in betaList:
            if ticker == item[0] and betaScore == -999:
                betaScore = item[1]
        if betaScore == -999:
            print(ticker)
            print("Ticker not found in beta list.")
        elif betaScore != "NaN":
            listClosePrices.append((listPrices, ticker, float(betaScore)))




print("Number of stocks read: " + str(len(listClosePrices)))
print("ADF limit: " + str(adfLimit))
print("Z threshold is: " + str(zthreshold))
for x in range(0,len(listClosePrices)-1):
    print(str(x) + " - " + str(listClosePrices[x][1]))

    print("Total crossings: " + str(totalCount))
    if totalCount > 0:
        print(100*round(midpointWinners10 / totalCount, 4))
        print(100*round(midpointWinners20 / totalCount, 4))
        print(100*round(midpointWinners30 / totalCount, 4))
        print(100*round(winners10day/totalCount,4))
        print(100*round(winners20day/totalCount,4))
        print(100*round(winners30day/totalCount,4))
        print("Beta distribution")
        print("10 Mid")
        for i in range(0,300):
            if beta10MidWinners[i] > 100:
                print(str(i)+" "+str(100 * round(beta10MidWinners[i] / betaCount[i], 4)))
        print("---------------------------------------")
        print("20 Mid")
        for i in range(0, 300):
            if beta20MidWinners[i] > 100:
                print(str(i)+" "+str(100 * round(beta20MidWinners[i] / betaCount[i], 4)))
        print("---------------------------------------")
        print("30 Mid")
        for i in range(0, 300):
            if beta30MidWinners[i] > 100:
                print(str(i)+" "+str(100 * round(beta30MidWinners[i] / betaCount[i], 4)))
        print("---------------------------------------")
        print("10 Full")
        for i in range(0, 300):
            if beta10Winners[i] > 100:
                print(str(i)+" "+str(100 * round(beta10Winners[i] / betaCount[i], 4)))
        print("---------------------------------------")
        print("20 Full")
        for i in range(0, 300):
            if beta20Winners[i] > 100:
                print(str(i)+" "+str(100 * round(beta20Winners[i] / betaCount[i], 4)))
        print("---------------------------------------")
        print("30 Full")
        for i in range(0, 300):
            if beta30Winners[i] > 100:
                print(str(i)+" "+str(100 * round(beta30Winners[i] / betaCount[i], 4)))

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
        adfValue = adf[0]
        betaDiff = round(100*abs(listClosePrices[x][2] - listClosePrices[y][2]))
        if adfValue < adfLimit and 0 < betaDiff < 300:
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
            # df = pd.DataFrame({'y': list1, 'x': list2})
            # result = coint_johansen(df, 0, 1)
            # theta = result.eig[0]
            # half_life = math.log(2) / theta
            # half_life = round(half_life)-6
            average = statistics.mean(ratioList)
            #print(stdv/abs(average))
            while index < len(zscoreList) - 31:
                index = index + 1
                if zscoreList[index] > zthreshold and zscoreList[index] == max(zscoreList[index-10:index+3]):
                    betaCount[betaDiff] = betaCount[betaDiff] + 1
                    currentCount = currentCount + 1

                    # index2 = index+1
                    # while zscoreList[index2 + 1] < zscoreList[index2] and (index2-index<10):
                    #     zturningPoint[index2-index] = zturningPoint[index2-index] + 1
                    #     index2 = index2 + 1
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
                        beta10Winners[betaDiff] = beta10Winners[betaDiff] + 1
                    if profit20 == True:
                        winners20day = winners20day + 1
                        beta20Winners[betaDiff] = beta20Winners[betaDiff] + 1
                    if profit30 == True:
                        winners30day = winners30day + 1
                        beta30Winners[betaDiff] = beta30Winners[betaDiff] + 1
                    if profit10mid == True:
                        midpointWinners10 = midpointWinners10 + 1
                        beta10MidWinners[betaDiff] = beta10MidWinners[betaDiff] + 1
                    if profit20mid == True:
                        midpointWinners20 = midpointWinners20 + 1
                        beta20MidWinners[betaDiff] = beta20MidWinners[betaDiff] + 1
                    if profit30mid == True:
                        midpointWinners30 = midpointWinners30 + 1
                        beta30MidWinners[betaDiff] = beta30MidWinners[betaDiff] + 1
                    # index2 = index
                    # while index2 < index+50 and index2 < len(zscoreList) and ratioList[index2+60] > average:
                    #     index2 = index2 + 1
                    # meanRevertCount[0] = meanRevertCount[0] + 1
                    # meanRevertTotal[0] = meanRevertTotal[0] + index2-index
                    # if 0 < half_life < 100:
                    #     halfLife3Count[half_life] = halfLife3Count[half_life] + 1
                    #     halfLife3Total[half_life] = halfLife3Total[half_life] + index2-index
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
                    betaCount[betaDiff] = betaCount[betaDiff] + 1
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
                        beta10Winners[betaDiff] = beta10Winners[betaDiff] + 1
                    if profit20 == True:
                        winners20day = winners20day + 1
                        beta20Winners[betaDiff] = beta20Winners[betaDiff] + 1
                    if profit30 == True:
                        winners30day = winners30day + 1
                        beta30Winners[betaDiff] = beta30Winners[betaDiff] + 1
                    if profit10mid == True:
                        midpointWinners10 = midpointWinners10 + 1
                        beta10MidWinners[betaDiff] = beta10MidWinners[betaDiff] + 1
                    if profit20mid == True:
                        midpointWinners20 = midpointWinners20 + 1
                        beta20MidWinners[betaDiff] = beta20MidWinners[betaDiff] + 1
                    if profit30mid == True:
                        midpointWinners30 = midpointWinners30 + 1
                        beta30MidWinners[betaDiff] = beta30MidWinners[betaDiff] + 1
                    # index2 = index
                    # while index2 < index + 50 and index2 < len(zscoreList) and ratioList[index2 + 60] < average:
                    #     index2 = index2 + 1
                    # meanRevertCount[0] = meanRevertCount[0] + 1
                    # meanRevertTotal[0] = meanRevertTotal[0] + index2 - index
                    # if 0 < half_life < 100:
                    #     halfLife3Count[half_life] = halfLife3Count[half_life] + 1
                    #     halfLife3Total[half_life] = halfLife3Total[half_life] + index2-index
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

