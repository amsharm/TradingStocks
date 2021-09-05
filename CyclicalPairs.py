import math
import statistics

import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import os.path


# masterIndex represents today
masterIndex = 250
lookBackPeriod = 1000
listClosePrices = []
listFiles = []
listVolumes = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.txt"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.txt"):
    listFiles.append(file)
for file in listFiles:
    f = open(file,"r")
    data = f.read()
    data2 = data.split("}")
    tempList = []
    listVolume = []
    if (len(data2) > lookBackPeriod):
        for i in range(1, lookBackPeriod + 1):
            tempList.append(float(data2[i].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip()))
            listVolume.append(float(data2[i].split("volume")[1].split(",")[0].replace('"', '').replace(':', '').strip()))
        tempList.reverse()
        listVolume.reverse()
        listClosePrices.append(((file.split(".txt")[0].split("s")[4].replace("\\", "")), tempList))
        listVolumes.append(((file.split(".txt")[0].split("s")[4].replace("\\", "")),listVolume))

outputList = []
for index in range(1,2):
    varLimit = index*.01
    summaryList = []
    numPositive = 0
    masterIndex = 250
    print(index)
    while masterIndex < 400:
        print(masterIndex)
        startIndex = masterIndex - 250
        currentNormalizedList = []
        for stock in listClosePrices:
            normalizedList = [stock[0],[1]]
            for i in range(startIndex,masterIndex):
                x = stock[1][i+1]
                y = stock[1][i]
                normalizedList[1].append((normalizedList[1][-1] * x / y))
            normalizedList[1].pop(0)
            currentNormalizedList.append(normalizedList)

        numEquities = len(currentNormalizedList)
        for firstStock in range(0,numEquities-1):
            for secondStock in range(firstStock + 1, numEquities):
                increasingordecreasing = 1
                maxes = []
                currentmax = 0

                for currentindex in range(0, 250):
                    if increasingordecreasing and abs(currentNormalizedList[firstStock][1][currentindex] - currentNormalizedList[secondStock][1][currentindex]) > currentmax:
                        currentmax = abs(currentNormalizedList[firstStock][1][currentindex] - currentNormalizedList[secondStock][1][currentindex])
                    elif increasingordecreasing:
                        maxes.append(currentmax)
                        increasingordecreasing = 0
                        currentmax = abs(currentNormalizedList[firstStock][1][currentindex] - currentNormalizedList[secondStock][1][currentindex])
                    elif abs(currentNormalizedList[firstStock][1][currentindex] - currentNormalizedList[secondStock][1][currentindex]) > currentmax:
                        increasingordecreasing = 1
                        currentmax = abs(currentNormalizedList[firstStock][1][currentindex] - currentNormalizedList[secondStock][1][currentindex])
                    else:
                        currentmax = abs(currentNormalizedList[firstStock][1][currentindex] - currentNormalizedList[secondStock][1][currentindex])
                if len(maxes) > 2 and increasingordecreasing == 1:
                    tempReturnList = []
                    if currentNormalizedList[firstStock][1][-1] > currentNormalizedList[secondStock][1][-1]:
                        firstStockIndex = firstStock
                        secondStockIndex = secondStock
                    else:
                        firstStockIndex = secondStock
                        secondStockIndex = firstStock
                    for day in range(1, 30):
                        tempReturnList.append(round(((listClosePrices[firstStockIndex][1][masterIndex] -
                                                      listClosePrices[firstStockIndex][1][masterIndex + day]) / (
                                                         listClosePrices[firstStockIndex][1][masterIndex]) + (
                                                             listClosePrices[secondStockIndex][1][masterIndex + day] -
                                                             listClosePrices[secondStockIndex][1][masterIndex]) / (
                                                         listClosePrices[secondStockIndex][1][masterIndex])), 3))
                    maxReturn = -1000
                    for returnval in tempReturnList:
                        if returnval > maxReturn:
                            maxReturn = returnval
                    variance = statistics.variance(maxes)
                    mean = statistics.mean(maxes)
                    if .03 < variance and mean > .3:
                        summaryList.append((variance,mean,maxReturn))
                        if maxReturn > 0:
                            numPositive = numPositive + 1
        masterIndex = masterIndex + 30
    outputList.append((varLimit,numPositive/len(summaryList)))
    print(numPositive/len(summaryList))
    print(len(summaryList))
print(outputList)
xpoints = []
ypoints = []
xpoints2 = []
# print(str(numPositive/len(summaryList)))
# print(len(summaryList))
# for item in summaryList:
#     xpoints.append(item[0])
#     xpoints2.append(item[1])
#     ypoints.append(item[2])
# plt.scatter(xpoints,ypoints,2)
# plt.show()
# plt.scatter(xpoints2,ypoints,2)
# plt.show()



