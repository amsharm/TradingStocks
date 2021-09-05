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

for x in range(0,numEquities-1):
    for y in range(x+1,numEquities):
        inDivergence = False
        highestx = listNormalizedPrices[x][1]
        highesty = listNormalizedPrices[y][1]
        for currentIndex in range(1,numDays-1):
            if listNormalizedPrices[x][currentIndex] > highestx:
                highestx = listNormalizedPrices[x][currentIndex]
            if listNormalizedPrices[y][currentIndex] > highesty:
                highesty = listNormalizedPrices[y][currentIndex]
            if inDivergence == False:
                if abs(listNormalizedPrices[x][currentIndex]-listNormalizedPrices[y][currentIndex]) > .4:
                    if listNormalizedPrices[x][currentIndex] > highestx or listNormalizedPrices[y][currentIndex] > highesty:
                        inDivergence = True
                        numDiverged = numDiverged + 1
                    else:
                        break
            else:
                if abs(listNormalizedPrices[x][currentIndex] - listNormalizedPrices[y][currentIndex]) < .3:
                    numClosedPairs = numClosedPairs + 1
                    break


print(str(numDiverged))
print(str(numClosedPairs))
