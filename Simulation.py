import statistics

import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import os.path


listFiles = []
listClosePrices = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.txt"):
    listFiles.append(file)

spy = open("C:/Users/17132/PycharmProjects/pythonProject/ETFs/SPY.txt","r").read().split("}")
spyprices = []


for file in listFiles:
    filesplit = open(file,"r").read().split("}")
    templist = []
    if len(filesplit) > 600:
        for i in range(1,600):
            templist.append(float(filesplit[i].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip()))
            spyprices.append(float(spy[i].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip()))
        templist.reverse()
        listClosePrices.append((templist,file))
tempList2 = []
spyprices.reverse()
currentCash = 10000

# [stock index in listclosePrices, number shares, price of purchase, day of purchase]
portfolio = []
numShortList = []
originalList = []
bollLimit = 3.5
durationHoldList = [0]
monthlyWinnings = 0
spyStartingPrice = spyprices[30]
inRecession = 0
for day in range(30,450):
    if currentCash > 1000:
        bollHighList = []
        bollLowList = []
        for i in range(0, len(listClosePrices)):
            boll = abs(listClosePrices[i][0][day] - statistics.mean(listClosePrices[i][0][day-19:day+1])) / statistics.stdev(listClosePrices[i][0][day-19:day+1])
            if boll < bollLimit:
                if listClosePrices[i][0][day] > statistics.mean(listClosePrices[i][0][day-19:day+1]):
                    bollHighList.append((boll,i,listClosePrices[i][0][day]))
                else:
                    bollLowList.append((boll,i,listClosePrices[i][0][day]))
        bollHighList.sort(key=itemgetter(0), reverse=True)
        bollLowList.sort(key=itemgetter(0),reverse = True)
        currentportFolioValue = 0
        for stock in portfolio:
            currentportFolioValue = currentportFolioValue + stock[1]*listClosePrices[stock[0]][0][day]
        numSharestoPurchase = round(currentCash/1000)
        if numSharestoPurchase == 0:
            numSharestoPurchase = 1
        cashPerStock = currentCash / numSharestoPurchase
        tempCash = currentportFolioValue
        numShortSharestoPurchase = 0
        numLongSharestoPurchase = 0
        for i in range(0,numSharestoPurchase):
            if tempCash > 0:
                numShortSharestoPurchase = numShortSharestoPurchase + 1
                tempCash = tempCash - cashPerStock
            else:
                numLongSharestoPurchase = numLongSharestoPurchase + 1
                tempCash = tempCash + cashPerStock
        #round(numSharestoPurchase/2)
        if currentportFolioValue == 0:
            for i in range(0,numLongSharestoPurchase):
                stockToBuy = bollLowList[i][1]
                sharesToBuy = cashPerStock/bollLowList[i][2]
                purchasePrice = bollLowList[i][2]
                portfolio.append((stockToBuy,sharesToBuy,purchasePrice,day))
                currentCash = currentCash - purchasePrice*sharesToBuy
                #print("Just bought -- " + str(sharesToBuy)+" shares of "+ str(stockToBuy) + " at " + str(purchasePrice) )
            for i in range(0,numShortSharestoPurchase):
                stockToBuy = bollHighList[i][1]
                sharesToBuy = -1*cashPerStock / bollHighList[i][2]
                purchasePrice = bollHighList[i][2]
                currentCash = currentCash + purchasePrice * sharesToBuy
                portfolio.append((stockToBuy,sharesToBuy,purchasePrice,day))
                #print("Just bought -- " + str(sharesToBuy) + " shares of " + str(stockToBuy) + " at " + str(purchasePrice))
        elif currentportFolioValue < 0:
            for i in range(0,numLongSharestoPurchase):
                stockToBuy = bollLowList[i][1]
                sharesToBuy = cashPerStock / bollLowList[i][2]
                purchasePrice = bollLowList[i][2]
                currentCash = currentCash - purchasePrice * sharesToBuy
                portfolio.append((stockToBuy, sharesToBuy, purchasePrice, day))
                #print("Just bought -- " + str(sharesToBuy) + " shares of " + str(stockToBuy) + " at " + str(purchasePrice))
        elif currentportFolioValue > 0:
            for i in range(0,numShortSharestoPurchase):
                stockToBuy = bollHighList[i][1]
                sharesToBuy = -1*cashPerStock / bollHighList[i][2]
                purchasePrice = bollHighList[i][2]
                currentCash = currentCash + purchasePrice * sharesToBuy
                portfolio.append((stockToBuy, sharesToBuy, purchasePrice, day))
                #print("Just bought -- " + str(sharesToBuy) + " shares of " + str(stockToBuy) + " at " + str(purchasePrice))
        #print("Current cash: " + str(currentCash))
    else:
        for index in reversed(range(0,len(portfolio))):
            stockToSell = portfolio[index][0]
            sharesToSell = portfolio[index][1]
            currentPrice = listClosePrices[portfolio[index][0]][0][day]
            purchasePrice = portfolio[index][2]
            # if (sharesToSell < 0 and (currentPrice - purchasePrice) > .2):
            #     print("STOP LOSS - Just sold -- " + str(sharesToSell) + " shares of " + str(stockToSell) + " at " + str(currentPrice) + "for a profit of " + str(sharesToSell*(currentPrice-purchasePrice)))
            #     currentCash = currentCash + sharesToSell*(currentPrice-purchasePrice) + -1*sharesToSell*purchasePrice
            #     print("Now cash value: " + str(currentCash))
            #     portfolio.pop(index)
            # elif (sharesToSell > 0 and (purchasePrice - currentPrice) > .2):
            #     print("STOP LOSS - Just sold -- " + str(sharesToSell) + " shares of " + str(stockToSell) + " at " + str(currentPrice) + "for a profit of " + str(sharesToSell*(currentPrice-purchasePrice)))
            #     currentCash = currentCash + sharesToSell * (currentPrice)
            #     print("Now cash value: " + str(currentCash))
            #     portfolio.pop(index)
            returnThreshold = .1
            if (sharesToSell < 0 and (purchasePrice - currentPrice) > returnThreshold):
                #print("Just sold -- " + str(sharesToSell) + " shares of " + str(stockToSell) + " at " + str(currentPrice) + "for a profit of " + str(sharesToSell*(currentPrice-purchasePrice)))
                currentCash = currentCash + -1*sharesToSell*purchasePrice + sharesToSell*(currentPrice-purchasePrice)
                #monthlyWinnings = monthlyWinnings + sharesToSell*(currentPrice-purchasePrice)
                #print("Now cash value: " + str(currentCash))
                durationHoldList.append(day - item[3])
                portfolio.pop(index)
            elif (sharesToSell > 0 and (currentPrice - purchasePrice) > returnThreshold):
                #print("Just sold -- " + str(sharesToSell) + " shares of " + str(stockToSell) + " at " + str(currentPrice) + "for a profit of " + str(sharesToSell*(currentPrice-purchasePrice)))
                currentCash = currentCash + sharesToSell * (currentPrice)
                #monthlyWinnings = monthlyWinnings + sharesToSell * (currentPrice-purchasePrice)
                #print("Now cash value: " + str(currentCash))
                durationHoldList.append(day - item[3])
                portfolio.pop(index)


    totalValue = currentCash
    numShort = 0

    for item in portfolio:
        #print(str(item[1]) + " shares of " + str(item[0]) + ", with a value of " + str(listClosePrices[item[0]][0][day]*item[1]))
        if item[1] > 0:
            totalValue = totalValue + item[1]*listClosePrices[item[0]][0][day]
        elif item[1] < 0:
            numShort = numShort + 1
            totalValue = totalValue + abs(item[1]*item[2]) + item[1]*(listClosePrices[item[0]][0][day]-listClosePrices[item[0]][0][item[3]])

    if day%1 == 0:
        #print("-------------------------------------")
        print(str(bollLimit) + " Current total value: " +str(totalValue) + " on day " + str(day-30) + " with pct short: "+str(numShort/len(portfolio)))
        spyvalue = 10000*(spyprices[day]/spyStartingPrice)
        #print(str(10000*(spyprices[day]/spyStartingPrice)))
        print(totalValue/spyvalue)
        #print(statistics.mean(durationHoldList))
        #print("-------------------------------------")
        monthlyWinnings = 0

# for item in listClosePrices:
#     boll = abs(item[0][249] - statistics.mean(item[0][230:250]))/statistics.stdev(item[0][230:250])
#     tempList2.append((boll,item[1]))
# tempList2.sort(key=itemgetter(0),reverse=True)
# for item in tempList2:
#     print(item)

# for i in range(0,len(listClosePrices)-1):
#     for j in range(i+1,len(listClosePrices)):
#         tempList = []
#         xpoints = range(1, 251)
#         for k in range(0,250):
#             tempList.append((listClosePrices[i][k]/listClosePrices[j][k])/spyprices[k])
#         totalRange = max(tempList) - min(tempList)
#         counter = 0
#         for k in range(0,47):
#             if max(tempList[k*5:k*5+20]) - min(tempList[k*5:k*5+20]) > .2*totalRange:
#                 counter = counter + 1
#         if counter > 45 and (max(tempList[225:250])-min(tempList[225:250])) > .3*totalRange and tempList[249] == max(tempList[150:250]):
#             print(listFiles[i])
#             print(listFiles[j])
#             normalized1 = [tempList[0]]
#             normalized2 = [tempList[0]]
#             normalized3 = [tempList[0]]
#             for index in range(1, 250):
#                 x1 = float(listClosePrices[i][index])
#                 y1 = float(listClosePrices[i][index - 1])
#                 x2 = float(listClosePrices[j][index])
#                 y2 = float(listClosePrices[j][index - 1])
#                 x3 = float(spyprices[index])
#                 y3 = float(spyprices[index - 1])
#                 normalized1.append(normalized1[-1] * x1 / y1)
#                 normalized2.append(normalized2[-1] * x2 / y2)
#                 normalized3.append(normalized3[-1] * x3 / y3)
#
#             plt.plot(xpoints, tempList)
#             # plt.plot(xpoints, normalized1)
#             # plt.plot(xpoints, normalized2)
#             # plt.plot(xpoints, normalized3)
#
#             plt.show()
