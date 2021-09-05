import statistics

import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

numDays = 250
listNormalizedPrices=[]
listnames=[]
listFiles = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.txt"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.txt"):
    listFiles.append(file)
for file in listFiles:
    f = open(file,"r")
    data = f.read()
    data2 = data.split("}")
    if len(data2) > numDays-2:
        listclose = []
        i = 1
        while (i < numDays):
            listclose.append(data2[i].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':','').strip())
            i = i + 1
        listclose.reverse()
        i = 1
        standardizedlist = [1]
        while (i < numDays-1):
            x = float(listclose[i])
            y = float(listclose[i - 1])
            standardizedlist.append(standardizedlist[-1] * x / y)
            i = i + 1
        listNormalizedPrices.append(standardizedlist)
        #listnames.append(file.split("Stocks")[1].split(".")[0])

numEquities = len(listNormalizedPrices)
print(str(numEquities))

totalNumPairs = 0
numClosedPairs = 0
numDiverged = 0
avgDaysClose = []
avgDifference = []
x = 0
y = 1
while (x < numEquities-1):
    y = x + 1
    while (y < numEquities):
        inDivergence = False
        diverged = False
        startingDay = 0
        runningDifference = 0
        for currentIndex in range(1,numDays-1):
            if inDivergence == False:
                runningDifference = runningDifference + abs(listNormalizedPrices[x][currentIndex] - listNormalizedPrices[y][currentIndex])
                if abs(listNormalizedPrices[x][currentIndex]-listNormalizedPrices[y][currentIndex]) > .4:
                    inDivergence = True
                    diverged = True
                    startingDay = currentIndex
            else:
                if abs(listNormalizedPrices[x][currentIndex] - listNormalizedPrices[y][currentIndex]) < .3:
                    inDivergence = False
                    days = currentIndex - startingDay
                    avgDaysClose.append(currentIndex-startingDay)
                    avgDifference.append(float(runningDifference)/float(startingDay))
                    break
        y = y+1
        totalNumPairs = totalNumPairs+1
        if diverged == True:
            numDiverged = numDiverged +1
        if inDivergence == False:
            numClosedPairs = numClosedPairs + 1
    x = x + 1

print(str(totalNumPairs))
print(str(numClosedPairs))
print(str(numDiverged))

print(str(100*numClosedPairs/totalNumPairs))
print(str(100*numDiverged/totalNumPairs))
print(str(100*(numClosedPairs-(totalNumPairs-numDiverged))/numDiverged))
print("-----------------")
print(len(avgDaysClose))
print(statistics.mean(avgDaysClose))
avgDaysClose.sort()
print(avgDaysClose)
bucket1 = 0
bucket2 = 0
bucket3 = 0
bucket4 = 0
bucket5 = 0
for item in avgDaysClose:
    if 0 < item < 12:
        bucket1 = bucket1 + 1
    elif 11 < item < 24:
        bucket2 = bucket2 + 1
    elif 23 < item < 35:
        bucket3 = bucket3 + 1
    elif 34 < item < 60:
        bucket4 = bucket4 + 1
    else:
        bucket5 = bucket5 + 1
print(bucket1/len(avgDaysClose))
print(bucket2/len(avgDaysClose))
print(bucket3/len(avgDaysClose))
print(bucket4/len(avgDaysClose))
print(bucket5/len(avgDaysClose))

