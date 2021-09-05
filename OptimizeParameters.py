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
import sys

def generateScoringFactors(inputList):
    tempTotalReturn = 0
    for item in inputList:
        tempTotalReturn = tempTotalReturn + item[0]
    averageReturn = tempTotalReturn/len(inputList)
    print("Average return: " + str(averageReturn))

    masterSumList = []
    masterCountList = []
    masterAverageList = []
    masterFactorList = []
    bollingerSumList = [0]*300
    bollingerCountList = [0]*300
    bollingerAverageList = [0] * 300
    bollingerFactorList = [0]*300
    volumeRatioSumList = [0]*500
    volumeRatioCountList = [0]*500
    volumeRatioAverageList = [0] * 500
    volumeRatioFactorList = [0]*500

    masterSumList.append([0]*300)
    masterSumList.append([0] * 300)
    masterSumList.append(bollingerSumList)
    masterSumList.append([0]*100)
    masterSumList.append(volumeRatioSumList)
    masterSumList.append([0]*200)
    masterSumList.append([0]*300)
    masterSumList.append([0] * 200)

    masterCountList.append([0] * 300)
    masterCountList.append([0] * 300)
    masterCountList.append(bollingerSumList)
    masterCountList.append([0] * 100)
    masterCountList.append(volumeRatioSumList)
    masterCountList.append([0] * 200)
    masterCountList.append([0] * 300)
    masterCountList.append([0] * 200)

    masterAverageList.append([0] * 300)
    masterAverageList.append([0] * 300)
    masterAverageList.append(bollingerSumList)
    masterAverageList.append([0] * 100)
    masterAverageList.append(volumeRatioSumList)
    masterAverageList.append([0] * 200)
    masterAverageList.append([0] * 300)
    masterAverageList.append([0] * 200)

    masterFactorList.append([0] * 300)
    masterFactorList.append([0] * 300)
    masterFactorList.append(bollingerSumList)
    masterFactorList.append([0] * 100)
    masterFactorList.append(volumeRatioSumList)
    masterFactorList.append([0] * 200)
    masterFactorList.append([0] * 300)
    masterFactorList.append([0] * 200)

    for item in inputList:
        roundedBollinger = int(100*round(item[3],2))
        roundedVolumeRatio = int(100*round(item[5],2))
        roundedTotalDistance = round(item[1])
        roundedFinalDistance = int(100*round(item[2],2))
        roundedSwitches = item[4]
        roundedVolume2 = round(item[6])
        roundedVariance = int(100*round(item[7],2))
        roundedMean = int(100*round(item[8],2))

        if -1 < roundedTotalDistance < 300:
            masterSumList[0][roundedTotalDistance] = masterSumList[0][roundedTotalDistance] + item[0]
            masterCountList[0][roundedTotalDistance] = masterCountList[0][roundedTotalDistance] + 1
        if -1 < roundedFinalDistance < 300:
            masterSumList[1][roundedFinalDistance] = masterSumList[1][roundedFinalDistance] + item[0]
            masterCountList[1][roundedFinalDistance] = masterCountList[1][roundedFinalDistance] + 1
        if -1 < roundedBollinger < 300:
            masterSumList[2][roundedBollinger] = masterSumList[2][roundedBollinger] + item[0]
            masterCountList[2][roundedBollinger] = masterCountList[2][roundedBollinger] + 1
        if -1 < roundedSwitches < 100:
            masterSumList[3][roundedSwitches] = masterSumList[3][roundedSwitches] + item[0]
            masterCountList[3][roundedSwitches] = masterCountList[3][roundedSwitches] + 1
        if -1 < roundedVolumeRatio < 500:
            masterSumList[4][roundedVolumeRatio] = masterSumList[4][roundedVolumeRatio] + item[0]
            masterCountList[4][roundedVolumeRatio] = masterCountList[4][roundedVolumeRatio] + 1
        if -1 < roundedVolume2 < 200:
            masterSumList[5][roundedVolume2] = masterSumList[5][roundedVolume2] + item[0]
            masterCountList[5][roundedVolume2] = masterCountList[5][roundedVolume2] + 1
        if -1 < roundedVariance < 300:
            masterSumList[6][roundedVariance] = masterSumList[6][roundedVariance] + item[0]
            masterCountList[6][roundedVariance] = masterCountList[6][roundedVariance] + 1
        if -1 < roundedMean < 200:
            masterSumList[7][roundedMean] = masterSumList[7][roundedMean] + item[0]
            masterCountList[7][roundedMean] = masterCountList[7][roundedMean] + 1

    for i in range(0,300):
        if masterCountList[0][i] > 0 and masterSumList[0][i] > 0:
            masterAverageList[0][i] = masterSumList[0][i]/masterCountList[0][i]
            masterFactorList[0][i] = round(masterAverageList[0][i]/averageReturn,3)
        if masterCountList[1][i] > 0 and masterSumList[1][i] > 0:
            masterAverageList[1][i] = masterSumList[1][i]/masterCountList[1][i]
            masterFactorList[1][i] = round(masterAverageList[1][i] / averageReturn, 3)
        if masterCountList[2][i] > 0 and masterSumList[2][i] > 0:
            masterAverageList[2][i] = masterSumList[2][i]/masterCountList[2][i]
            masterFactorList[2][i] = round(masterAverageList[2][i] / averageReturn, 3)
    for i in range(0,100):
        if masterCountList[3][i] > 0 and masterSumList[3][i] > 0:
            masterAverageList[3][i] = masterSumList[3][i]/masterCountList[3][i]
            masterFactorList[3][i] = round(masterAverageList[3][i] / averageReturn, 3)
    for i in range(0,500):
        if masterCountList[4][i] > 0 and masterSumList[4][i] > 0:
            masterAverageList[4][i] = masterSumList[4][i] / masterCountList[4][i]
            masterFactorList[4][i] = round(masterAverageList[4][i] / averageReturn, 3)
    for i in range(0,200):
        if masterCountList[5][i] > 0 and masterSumList[5][i] > 0:
            masterAverageList[5][i] = masterSumList[5][i] / masterCountList[5][i]
            masterFactorList[5][i] = round(masterAverageList[5][i] / averageReturn, 3)
    for i in range(0,300):
        if masterCountList[6][i] > 0 and masterSumList[6][i] > 0:
            masterAverageList[6][i] = masterSumList[6][i] / masterCountList[6][i]
            masterFactorList[6][i] = round(masterAverageList[6][i] / averageReturn, 3)
    for i in range(0,200):
        if masterCountList[7][i] > 0 and masterSumList[7][i] > 0:
            masterAverageList[7][i] = masterSumList[7][i] / masterCountList[7][i]
            masterFactorList[7][i] = round(masterAverageList[7][i] / averageReturn, 3)

    for i in range(0,8):
        print(masterFactorList[i])

def optimize(inputList):
    length = len(inputList[0])
    for masterIndex in range(1, length):
        for volumeThreshold in range(1,10):
            print(str(masterIndex) + " --- " + str(.1*volumeThreshold))
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
            print(len(oneBucket))
            for item in inputList:
                tempindex = math.floor((item[masterIndex] - minValue)/increment)
                if tempindex > len(oneBucket)-1:
                    tempindex = len(oneBucket) - 1
                if item[0] == 0:
                    zeroBucket[tempindex] = zeroBucket[tempindex] + 1
                else:
                    oneBucket[tempindex] = oneBucket[tempindex] + 1
            lossPercentage = sum(zeroBucket)/(sum(oneBucket) + sum(zeroBucket))
            winPercentage = sum(oneBucket)/(sum(oneBucket) + sum(zeroBucket))
            print("The current win percentage is " + str(winPercentage))
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
                    if currentZeroSum + currentOneSum < ((.1*volumeThreshold)*(len(inputList))):
                        newWinPct = (totalOnes - currentOneSum)/(totalOnes + totalZeros - currentOneSum - currentZeroSum)
                        if newWinPct > winPercentage:
                            listRevisedWinLoss.append((newWinPct,round(condensedList[index][0] * increment + minValue,2), round(condensedList[index2][0] * increment+minValue,2), round((currentZeroSum+currentOneSum)/(totalZeros+totalOnes),3)))
            listRevisedWinLoss.sort(key = itemgetter(0), reverse=True)
            print(listRevisedWinLoss[0:5])

# masterIndex represents today
masterIndex = 250
lookBackPeriod = 251
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

summaryList = []
totalSampleSize = 0
negativeList = [0]
positiveList = [0]
completeList =[0]
while masterIndex < 251:
    print(str(int(100*(masterIndex - 250)/(900-250)))+" - "+str(len(summaryList)))
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
            totalSampleSize = totalSampleSize + 1
            finalswitch = 0
            totalswitches = 0
            totaldistance = 0
            increasingordecreasing = 1
            maxes = []
            currentmax = 0
            if currentNormalizedList[firstStock][1][0] > currentNormalizedList[secondStock][1][0]:
                currentlarger = 0
            else:
                currentlarger = 1
            for currentindex in range(0, 250):
                totaldistance = totaldistance + abs(currentNormalizedList[firstStock][1][currentindex] - currentNormalizedList[secondStock][1][currentindex])
                if currentNormalizedList[firstStock][1][currentindex] > currentNormalizedList[secondStock][1][currentindex]:
                    if currentlarger == 1:
                        totalswitches = totalswitches + 1
                        currentlarger = 0
                        finalswitch = currentindex
                else:
                    if currentlarger == 0:
                        totalswitches = totalswitches + 1
                        currentlarger = 1
                        finalswitch = currentindex
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
            finaldistance = abs(currentNormalizedList[firstStock][1][-1] - currentNormalizedList[secondStock][1][-1])

            if currentNormalizedList[firstStock][1][-1] > currentNormalizedList[secondStock][1][-1]:
                firstStockIndex = firstStock
                secondStockIndex = secondStock
            else:
                firstStockIndex = secondStock
                secondStockIndex = firstStock

            if len(maxes) > 2 and finalswitch > 180 and totaldistance < 20:
            #if len(maxes) > 2:
            #if len(maxes) > 2:
                bollingerScore = 0
                lastTwentyx = listClosePrices[firstStockIndex][1][(masterIndex - 20):masterIndex]
                lastTwentyy = listClosePrices[secondStockIndex][1][(masterIndex - 20):masterIndex]
                bollingerScore = ((listClosePrices[firstStockIndex][1][masterIndex] - statistics.mean(lastTwentyx)) / (
                        2 * statistics.stdev(lastTwentyx))) + ((statistics.mean(lastTwentyy) -
                                                                listClosePrices[secondStockIndex][1][masterIndex]) / (
                                                                       2 * statistics.stdev(lastTwentyy)))
                # tempRatio = statistics.variance(lastTwentyx)/statistics.variance(listClosePrices[firstStockIndex][1][(masterIndex-40):(masterIndex-20)]) + statistics.variance(lastTwentyy) / statistics.variance(listClosePrices[secondStockIndex][1][(masterIndex - 40):(masterIndex - 20)])
                # tempvariance = statistics.variance(lastTwentyy) + statistics.variance(lastTwentyx)
                # if secondStockIndex == 108:
                #     print(currentNormalizedList[108][0])
                #     print(listClosePrices[108][1][masterIndex])
                #     print(statistics.mean(lastTwentyy))
                #     print(((statistics.mean(lastTwentyy) - listClosePrices[secondStockIndex][1][masterIndex]) / (
                #                                                        2 * statistics.stdev(lastTwentyy))))
                variance = 0
                mean = 0
                volumeRatio = 0
                # variance = statistics.variance(maxes)
                # mean = statistics.mean(maxes)
                tempReturnList = []
                tempReturnList20 = []
                tempReturnList10 = []
                # for day in range(1, 10):
                #     tempReturnList.append(round(((listClosePrices[firstStockIndex][1][masterIndex] -
                #                            listClosePrices[firstStockIndex][1][masterIndex + day]) / (
                #                           listClosePrices[firstStockIndex][1][masterIndex]) + (
                #                                       listClosePrices[secondStockIndex][1][masterIndex + day] -
                #                                       listClosePrices[secondStockIndex][1][masterIndex]) / (
                #                           listClosePrices[secondStockIndex][1][masterIndex])), 3))
                # for day in range(1, 20):
                #     tempReturnList20.append(round(((listClosePrices[firstStockIndex][1][masterIndex] -
                #                            listClosePrices[firstStockIndex][1][masterIndex + day]) / (
                #                           listClosePrices[firstStockIndex][1][masterIndex]) + (
                #                                       listClosePrices[secondStockIndex][1][masterIndex + day] -
                #                                       listClosePrices[secondStockIndex][1][masterIndex]) / (
                #                           listClosePrices[secondStockIndex][1][masterIndex])), 3))
                # for day in range(1, 10):
                #     tempReturnList10.append(round(((listClosePrices[firstStockIndex][1][masterIndex] -
                #                            listClosePrices[firstStockIndex][1][masterIndex + day]) / (
                #                           listClosePrices[firstStockIndex][1][masterIndex]) + (
                #                                       listClosePrices[secondStockIndex][1][masterIndex + day] -
                #                                       listClosePrices[secondStockIndex][1][masterIndex]) / (
                #                           listClosePrices[secondStockIndex][1][masterIndex])), 3))

                meanVolume = 0
                volumeRatio2 = 0
                lastHundredVx = statistics.mean(listVolumes[firstStockIndex][1][(masterIndex - 100):masterIndex])
                lastTwentyVx = listVolumes[firstStockIndex][1][(masterIndex - 20):masterIndex]
                lastHundredVy = statistics.mean(listVolumes[secondStockIndex][1][(masterIndex - 100):masterIndex])
                lastTwentyVy = listVolumes[secondStockIndex][1][(masterIndex - 20):masterIndex]
                volumeRatio = statistics.mean(lastTwentyVx) / lastHundredVx + statistics.mean(lastTwentyVy) / lastHundredVy

                # volumeRatio2Sumx = 0
                # volumeRatio2Sumy = 0
                # volumeCounter = 0
                # try:
                #     for number in range(5,len(lastTwentyVx)):
                #         volumeRatio2Sumx = volumeRatio2Sumx + lastTwentyVx[number]/lastTwentyVx[number-5]
                #         volumeRatio2Sumy = volumeRatio2Sumy + lastTwentyVy[number]/lastTwentyVy[number-5]
                #         volumeCounter = volumeCounter + 1
                #     volumeRatio2 = .1*(volumeRatio2Sumy + volumeRatio2Sumx)/volumeCounter
                #     meanVolume = statistics.mean(lastTwentyVy) + statistics.mean(lastTwentyVx)

                # except:
                #     pass

                #if 2.56 > bollingerScore > 1.43 and (volumeRatio < 1.27 or volumeRatio > 2.86):
                if 3 > bollingerScore > 1.43 and (volumeRatio < 1.27 or volumeRatio > 2.86):
                #if 2.6 > bollingerScore > 2.2:
                    # completeList.append(tempvariance)
                    # if max(tempReturnList) < .05:
                    #     negativeList.append(tempvariance)
                    # else:
                    #     positiveList.append(tempvariance)
                    # if len(completeList) % 100 == 0:
                    #     print(statistics.mean(positiveList))
                    #     print(statistics.mean(completeList))
                    #     print(statistics.mean(negativeList))
                    #     print("---------------------")
                #if volumeRatio < 1.27 or volumeRatio > 2.86:

                    summaryList.append((firstStockIndex, currentNormalizedList[firstStockIndex][0], secondStockIndex,
                                    currentNormalizedList[secondStockIndex][0], round(totaldistance,2), round(finaldistance,3),
                                    tempReturnList,bollingerScore,totalswitches,finalswitch,volumeRatio,volumeRatio2, variance,
                                    mean, meanVolume, increasingordecreasing,tempReturnList20, tempReturnList10))

    masterIndex = masterIndex + 30

newList = []

print("Total Sample Size: " + str(totalSampleSize))
print(len(summaryList))
counter = 0
numPositive = 0
num5 = 0
num10 = 0
summaryList.sort(key=itemgetter(7),reverse=True)
for item in summaryList:
    print(item)
exit()
for item in summaryList:
    counter = counter + 1
    if counter%100000 == 0:
        print(counter)
    max = -100
    numDays = 0
    days = 0

    for returnValue in item[6]:
        days = days + 1
        if returnValue > max:
            numDays = days
            max = returnValue
    if max > 0:
        numPositive = numPositive + 1
    if max > .02:
        newList.append((item[4],item[5],round(item[7],3), item[8], item[9],max,round((1000*max/numDays),2),item[10],item[11], item[12], item[13],item[14]))
    if max > .05:
        num5 = num5 + 1
    if max > .1:
        num10 = num10 + 1
#newnewList.append((1,item[0],item[1],item[2],item[3],item[4].item[7],item[8],item[9],item[10],item[11]))

print(str(numPositive/len(summaryList)))
print(str(len(newList)/len(summaryList)))
print(str(num5/len(summaryList)))
print(str(num10/len(summaryList)))

newnewList = []

# for item in newList:
#     newnewList.append((item[6],item[0],item[1],item[2],item[3],item[7],item[8],item[9],item[10]))
# generateScoringFactors(newnewList)
# for item in newList:
#     if item[5] > 0:
#         newnewList.append((1,item[0],item[1],item[2],item[3],item[4],item[7],item[8],item[9],item[10],item[11]))
#     else:
#         newnewList.append((0, item[0], item[1], item[2],item[3], item[4],item[7], item[8], item[9], item[10], item[11]))

# for item in newList:
#     if item[5] > 0:
#         newnewList.append((1,item[7]))
#     else:
#         newnewList.append((0, item[7]))

# optimize(newnewList)

exit()

xpoints1 = []
xpoints1avg = []
ypoints1avg = [0]
xpoints2 = []
xpoints2avg = []
ypoints2avg = [0]
ypoints = []
xpoints3 = []
xpoints3avg = []
ypoints3avg = [0]
xpoints4 = []
xpoints4avg = []
ypoints4avg = [0]
xpoints5 = []
xpoints5avg = []
xpoints6 = []
xpoints7 = []
xpoints8 = []
xpoints9 = []
xpoints10 = []
ypoints5avg = [0]
xpoints6avg = []
ypoints6avg = [0]
xpoints7avg = []
xpoints8avg = []
xpoints9avg = []
ypoints7avg = [0]
ypoints8avg = [0]
ypoints9avg = [0]
ypoints2 = []
ypoints1ratio = [0]
ypoints2ratio = [0]
ypoints3ratio = [0]
ypoints4ratio = [0]
ypoints5ratio = [0]
ypoints6ratio = [0]
ypoints7ratio = [0]
ypoints8ratio = [0]
ypoints9ratio = [0]

min1 = 0
max1 = 800
min2 = 0
max2 = 8
min3 = -3
max3 = 4
min4 = 0
max4 = 41
min5 = 0
max5 = 251
min6 = 0
max6 = 8.1
min7 = 0
max7 = 4.1
min8 = 0
max8 = 5.1
min9 = 0
max9 = 5.1

numIntervals = 100

for i in range(1, numIntervals + 1):
    xpoints1avg.append(min1 + ((i * (max1 - min1) / numIntervals)))
    xpoints2avg.append(min2 + ((i * (max2 - min2) / numIntervals)))
    xpoints3avg.append(min3 + ((i * (max3 - min3) / numIntervals)))
    xpoints4avg.append(min4 + ((i * (max4 - min4) / numIntervals)))
    xpoints5avg.append(min5 + ((i * (max5 - min5) / numIntervals)))
    xpoints6avg.append(min6 + ((i * (max6 - min6) / numIntervals)))
    xpoints7avg.append(min7 + ((i * (max7 - min7) / numIntervals)))
    xpoints8avg.append(min8 + ((i * (max8 - min8) / numIntervals)))
    xpoints9avg.append(min9 + ((i * (max9 - min9) / numIntervals)))

for i in range(1, numIntervals):
    if i%10 == 0:
        print(i)
    sum1 = 0
    count1 = 0
    sum2 = 0
    count2 = 0
    sum3 = 0
    count3 = 0
    sum4 = 0
    count4 = 0
    sum5 = 0
    count5 = 0
    sum6 = 0
    count6 = 0
    sum7 = 0
    count7 = 0
    sum8 = 0
    count8 = 0
    sum9 = 0
    count9 = 0
    winners = [0,0,0,0,0,0,0,0,0]
    losers = [0,0,0,0,0,0,0,0,0]
    for item in newList:
        if xpoints1avg[i-1] < item[0] < xpoints1avg[i]:
            sum1 = sum1 + item[6]
            count1 = count1 + 1
            if item[5] > 0:
                winners[0] = winners[0] + 1
            else:
                losers[0] = losers[0] + 1
        if xpoints2avg[i-1] < item[1] < xpoints2avg[i]:
            sum2 = sum2 + item[6]
            count2 = count2 + 1
            if item[5] > 0:
                winners[1] = winners[1] + 1
            else:
                losers[1] = losers[1] + 1
        if xpoints3avg[i-1] < item[2] < xpoints3avg[i]:
            sum3 = sum3 + item[6]
            count3 = count3 + 1
            if item[5] > 0:
                winners[2] = winners[2] + 1
            else:
                losers[2] = losers[2] + 1
        if xpoints4avg[i-1] < item[3] < xpoints4avg[i]:
            sum4 = sum4 + item[6]
            count4 = count4 + 1
            if item[5] > 0:
                winners[3] = winners[3] + 1
            else:
                losers[3] = losers[3] + 1
        if xpoints5avg[i-1] < item[4] < xpoints5avg[i]:
            sum5 = sum5 + item[6]
            count5 = count5 + 1
            if item[5] > 0:
                winners[4] = winners[4] + 1
            else:
                losers[4] = losers[4] + 1
        if xpoints6avg[i-1] < item[7] < xpoints6avg[i]:
            sum6 = sum6 + item[6]
            count6 = count6 + 1
            if item[5] > 0:
                winners[5] = winners[5] + 1
            else:
                losers[5] = losers[5] + 1
        if xpoints7avg[i-1] < item[8] < xpoints7avg[i]:
            sum7 = sum7 + item[6]
            count7 = count7 + 1
            if item[5] > 0:
                winners[6] = winners[6] + 1
            else:
                losers[6] = losers[6] + 1
        if xpoints8avg[i-1] < item[9] < xpoints8avg[i]:
            sum8 = sum8 + item[6]
            count8 = count8 + 1
            if item[5] > 0:
                winners[7] = winners[7] + 1
            else:
                losers[7] = losers[7] + 1
        if xpoints9avg[i-1] < item[10] < xpoints9avg[i]:
            sum9 = sum9 + item[6]
            count9 = count9 + 1
            if item[5] > 0:
                winners[8] = winners[8] + 1
            else:
                losers[8] = losers[8] + 1

    if count1 > 0:
        ypoints1avg.append(round((sum1/count1),2))
        ypoints1ratio.append(100*winners[0] / (winners[0] + losers[0]))
    else:
        ypoints1avg.append(ypoints1avg[-1])
        ypoints1ratio.append(ypoints1ratio[-1])
    if count2 > 0:
        ypoints2avg.append(round((sum2 / count2), 2))
        ypoints2ratio.append(100*winners[1] / (winners[1] + losers[1]))
    else:
        ypoints2avg.append(ypoints2avg[-1])
        ypoints2ratio.append(ypoints2ratio[-1])
    if count3 > 0:
        ypoints3avg.append(round((sum3 / count3), 2))
        ypoints3ratio.append(100*winners[2] / (winners[2] + losers[2]))
    else:
        ypoints3avg.append(ypoints3avg[-1])
        ypoints3ratio.append(ypoints3ratio[-1])
    if count4 > 0:
        ypoints4avg.append(round((sum4 / count4), 2))
        ypoints4ratio.append(100*winners[3] / (winners[3] + losers[3]))
    else:
        ypoints4avg.append(ypoints4avg[-1])
        ypoints4ratio.append(ypoints4ratio[-1])
    if count5 > 0:
        ypoints5avg.append(round((sum5 / count5), 2))
        ypoints5ratio.append(100*winners[4] / (winners[4] + losers[4]))
    else:
        ypoints5avg.append(ypoints5avg[-1])
        ypoints5ratio.append(ypoints5ratio[-1])
    if count6 > 0:
        ypoints6avg.append(round((sum6 / count6), 2))
        ypoints6ratio.append(100*winners[5] / (winners[5] + losers[5]))
    else:
        ypoints6avg.append(ypoints6avg[-1])
        ypoints6ratio.append(ypoints6ratio[-1])
    if count7 > 0:
        ypoints7avg.append(round((sum7 / count7), 2))
        ypoints7ratio.append(100*winners[6] / (winners[6] + losers[6]))
    else:
        ypoints7avg.append(ypoints7avg[-1])
        ypoints7ratio.append(ypoints7ratio[-1])
    if count8 > 0:
        ypoints8avg.append(round((sum8 / count8), 2))
        ypoints8ratio.append(100*winners[7] / (winners[7] + losers[7]))
    else:
        ypoints8avg.append(ypoints8avg[-1])
        ypoints8ratio.append(ypoints8ratio[-1])
    if count9 > 0:
        ypoints9avg.append(round((sum9 / count9), 2))
        ypoints9ratio.append(100*winners[8] / (winners[8] + losers[8]))
    else:
        ypoints9avg.append(ypoints9avg[-1])
        ypoints9ratio.append(ypoints9ratio[-1])

for item in newList:
    if item[5] < 2:
        xpoints1.append(item[0])
        xpoints2.append(item[1])
        xpoints3.append(item[2])
        xpoints4.append(item[3])
        xpoints5.append(item[4])
        xpoints6.append(item[7])
        xpoints7.append(item[8])
        xpoints8.append(item[9])
        xpoints9.append(item[10])
        xpoints10.append(item[11])
        ypoints.append(item[5])
        ypoints2.append(item[6])

plt.scatter(xpoints1,ypoints,2)
plt.show()
plt.scatter(xpoints1,ypoints2,2)
plt.show()
plt.scatter(xpoints1avg,ypoints1avg)
plt.show()
plt.scatter(xpoints1avg,ypoints1ratio)
plt.show()
plt.scatter(xpoints2,ypoints,2)
plt.show()
plt.scatter(xpoints2,ypoints2,2)
plt.show()
plt.scatter(xpoints2avg,ypoints2avg)
plt.show()
plt.scatter(xpoints2avg,ypoints2ratio)
plt.show()
plt.scatter(xpoints3,ypoints,2)
plt.show()
plt.scatter(xpoints3,ypoints2,2)
plt.show()
plt.scatter(xpoints3avg,ypoints3avg)
plt.show()
plt.scatter(xpoints3avg,ypoints3ratio)
plt.show()
plt.scatter(xpoints4,ypoints,2)
plt.show()
plt.scatter(xpoints4,ypoints2,2)
plt.show()
plt.scatter(xpoints4avg,ypoints4avg)
plt.show()
plt.scatter(xpoints4avg,ypoints4ratio)
plt.show()
plt.scatter(xpoints5,ypoints,2)
plt.show()
plt.scatter(xpoints5,ypoints2,2)
plt.show()
plt.scatter(xpoints5avg,ypoints5avg)
plt.show()
plt.scatter(xpoints5avg,ypoints5ratio)
plt.show()
plt.scatter(xpoints6,ypoints,2)
plt.show()
plt.scatter(xpoints6,ypoints2,2)
plt.show()
plt.scatter(xpoints6avg,ypoints6avg)
plt.show()
plt.scatter(xpoints6avg,ypoints6ratio)
plt.show()
plt.scatter(xpoints7,ypoints,2)
plt.show()
plt.scatter(xpoints7,ypoints2,2)
plt.show()
plt.scatter(xpoints7avg,ypoints7avg)
plt.show()
plt.scatter(xpoints7avg,ypoints7ratio)
plt.show()
plt.scatter(xpoints8,ypoints,2)
plt.show()
plt.scatter(xpoints8,ypoints2,2)
plt.show()
plt.scatter(xpoints8avg,ypoints8avg)
plt.show()
plt.scatter(xpoints8avg,ypoints8ratio)
plt.show()
plt.scatter(xpoints9,ypoints,2)
plt.show()
plt.scatter(xpoints9,ypoints2,2)
plt.show()
plt.scatter(xpoints9avg,ypoints9avg)
plt.show()
plt.scatter(xpoints9avg,ypoints9ratio)
plt.show()
plt.scatter(xpoints10,ypoints,2)
plt.show()
plt.scatter(xpoints10,ypoints2,2)
plt.show()