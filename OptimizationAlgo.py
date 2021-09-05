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


def optimize(inputList):
    length = len(inputList[0])
    for masterIndex in range(1, length):
        maxValue = -100000
        minValue = 100000
        for item in inputList:
            if item[masterIndex] > maxValue:
                maxValue = item[masterIndex]
            if item[masterIndex] < minValue:
                minValue = item[masterIndex]
        zeroBucket = [0]*1001
        oneBucket = [0]*1001
        increment = (maxValue - minValue)/1001
        for item in inputList:
            if item[0] == 0:
                zeroBucket[math.floor((item[masterIndex] - minValue)/increment)] = zeroBucket[math.floor((item[masterIndex] - minValue)/increment)] + 1
            else:
                oneBucket[math.floor((item[masterIndex] - minValue)/increment)] = oneBucket[math.floor((item[masterIndex] - minValue)/increment)] + 1
        lossPercentage = sum(zeroBucket)/(sum(oneBucket) + sum(zeroBucket))
        winPercentage = sum(oneBucket)/(sum(oneBucket) + sum(zeroBucket))
        print("The current loss percentage is " + str(lossPercentage))
        proportionList = []
        for i in range(0,len(zeroBucket)):
            if (zeroBucket[i] > 0 or oneBucket[i] > 0) and (zeroBucket[i]/(zeroBucket[i]+oneBucket[i])) > lossPercentage:
                proportionList.append((i,zeroBucket[i],oneBucket[i]))
        condensedList = []
        i = 0
        lastIndex = proportionList[0][0]
        i = 1
        startingIndex = lastIndex
        endIndex = lastIndex
        while i < len(proportionList):
            if proportionList[i][0] == lastIndex + 1:
                lastIndex = lastIndex + 1
                endIndex = endIndex + 1
            else:
                lastIndex = proportionList[i][0]
                condensedList.append((startingIndex,endIndex))
                startingIndex = lastIndex
                endIndex = lastIndex
            i = i + 1
        condensedList.append((startingIndex, endIndex))
        totalZeros = sum(zeroBucket)
        totalOnes = sum(oneBucket)
        listRevisedWinLoss = []
        for index in range(0, len(condensedList)-1):
            for index2 in range(index+1,len(condensedList)):
                currentOneSum = sum(oneBucket[condensedList[index][0]:(condensedList[index2][0]+1)])
                currentZeroSum = sum(zeroBucket[condensedList[index][0]:(condensedList[index2][0]+1)])
                if currentZeroSum + currentOneSum < 4:
                    newWinPct = (totalOnes - currentOneSum)/(totalOnes + totalZeros - currentOneSum - currentZeroSum)
                    if newWinPct > winPercentage:
                        listRevisedWinLoss.append((newWinPct,round(condensedList[index][0] * increment + minValue,2), round(condensedList[index2][0] * increment+minValue,2)))
        listRevisedWinLoss.sort(key = itemgetter(0), reverse=True)
        print(masterIndex)
        print(listRevisedWinLoss[0:5])

testList = []
testList.append((1,5))
testList.append((1,6))
testList.append((1,10))
testList.append((1,11))
testList.append((1,12))
testList.append((0,7))
testList.append((0,8))
testList.append((0,9))
testList.append((0,4))
testList.append((0,13))

optimize(testList)


