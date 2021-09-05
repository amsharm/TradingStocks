import math
import statistics
import datetime as dt
import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import os.path
import statsmodels.api as sm
import csv
import GetMinuteYahooData

GetMinuteYahooData.exec()

time.sleep(1)
listFiles = []
listnames = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/MinuteData/*.csv"):
    listFiles.append(file)
listClosePrices = []


for file in listFiles:
    tempList = []
    with open(file, "r") as inputfile:
        csvreader = csv.reader(inputfile)
        header = next(csvreader)
        for row in csvreader:
            try:
                tempList.append((row[0],float(row[5])))
            except:
                print("blank: " + str(row[5]))

        listClosePrices.append(tempList)

listDates = []
listLength = len(listClosePrices[0])
for item in listClosePrices:
    print(len(item))
if len(listClosePrices[0]) == len(listClosePrices[0]):
    for item in listClosePrices[0]:
        listDates.append(item[0])
else:
    print("IVV list is not complete. choose another")
    exit()

newListClosePrices = []
print(len(listDates))
for item in listClosePrices:
    if len(item) == listLength:
        tempList = []
        for row in item:
            tempList.append(row[1])
        newListClosePrices.append(tempList)
    else:
        newList = []
        dateIndex = 0
        priceIndex = 0
        while priceIndex < len(item) and dateIndex < len(listDates):
            if item[priceIndex][0] == listDates[dateIndex]:
                newList.append(item[priceIndex][1])
                dateIndex = dateIndex + 1
                priceIndex = priceIndex + 1
            else:
                newList.append(newList[-1])
                dateIndex = dateIndex + 1
        print(len(newList))
        newListClosePrices.append(newList)

listIVV = newListClosePrices[0]
listSCHO = newListClosePrices[1]
listSPLG = newListClosePrices[2]
listVGSH = newListClosePrices[3]
listVOO = newListClosePrices[4]
#
# xpoints = range(0,listLength)
# print("IVV")
# plt.plot(xpoints,listIVV)
# plt.show()
# print("SCHO")
# plt.plot(xpoints,listSCHO)
# plt.show()
# print("SPLG")
# plt.plot(xpoints,listSPLG)
# plt.show()
# print("VGSH")
# plt.plot(xpoints,listVGSH)
# plt.show()
# print("VOO")
# plt.plot(xpoints,listVOO)
# plt.show()

modelSPLGVOO = sm.OLS(listSPLG, listVOO)
hedgeRatioSPLGVOO = modelSPLGVOO.fit().params[0]
print("Hedge ratio for SPLG-VOO: " + str(hedgeRatioSPLGVOO))

modelIVVSPLG = sm.OLS(listIVV, listSPLG)
hedgeRatioIVVSPLG = modelIVVSPLG.fit().params[0]
print("Hedge ratio for IVV-SPLG: " + str(hedgeRatioIVVSPLG))

modelSCHOVGSH = sm.OLS(listSCHO, listVGSH)
hedgeRatioSCHOVGSH = modelSCHOVGSH.fit().params[0]
print("Hedge ratio for SCHO-VGSH: " + str(hedgeRatioSCHOVGSH))


ratioList1 = []
ratioList2 = []
ratioList3 = []
for i in range(0, listLength):
    ratioList1.append(listSPLG[i] - hedgeRatioSPLGVOO * listVOO[i])
    ratioList2.append(listIVV[i] - hedgeRatioIVVSPLG * listSPLG[i])
    ratioList3.append(listSCHO[i] - hedgeRatioSCHOVGSH * listVGSH[i])

print("SPLG-VOO")
plt.figure(figsize=(15, 7))
xpoints = range(0,listLength)
plt.plot(xpoints,ratioList1)
plt.axhline(0, color="red")
plt.show()
plt.figure(figsize=(15, 7))
xpoints = range(listLength-300,listLength)
plt.axhline(0, color="red")
ratioList1 = ratioList1[listLength-300:listLength]
plt.plot(xpoints,ratioList1)

plt.show()

print("IVV-SPLG")
xpoints = range(0,listLength)
plt.plot(xpoints,ratioList2)
plt.show()
plt.figure(figsize=(15, 7))
xpoints = range(listLength-300,listLength)
ratioList2 = ratioList2[listLength-300:listLength]
plt.plot(xpoints,ratioList2)
plt.axhline(0, color="red")
plt.show()

print("SCHO-VGSH")
xpoints = range(0,listLength)
plt.plot(xpoints,ratioList3)
plt.show()
plt.figure(figsize=(15, 7))
xpoints = range(listLength-300,listLength)
ratioList3 = ratioList3[listLength-300:listLength]
plt.plot(xpoints,ratioList3)
plt.axhline(0, color="red")
plt.show()


