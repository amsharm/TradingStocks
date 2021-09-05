# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import statistics

import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import os.path

for i in range(0,10):
    print(i)
    if i%3 == 0:
        i = i-1

exit()

numNegativeMonths = 0
positiveReturn = []
# symbolA is the short position. symbolB is the long position
# period should be less than numDaysAgo
def getOneMonthReturn(symbolA, symbolB, numDaysAgo,period):
    if os.path.isfile("C:/Users/17132/PycharmProjects/pythonProject/ETFs/" + symbolA + ".txt"):
        f = open("C:/Users/17132/PycharmProjects/pythonProject/ETFs/" + symbolA + ".txt", "r")
    else:
        f = open("C:/Users/17132/PycharmProjects/pythonProject/Stocks/" + symbolA + ".txt", "r")

    if os.path.isfile("C:/Users/17132/PycharmProjects/pythonProject/ETFs/" + symbolB + ".txt"):
        g = open("C:/Users/17132/PycharmProjects/pythonProject/ETFs/" + symbolB + ".txt", "r")
    else:
        g = open("C:/Users/17132/PycharmProjects/pythonProject/Stocks/" + symbolB + ".txt", "r")
    dataf = f.read().split("}")
    datag = g.read().split("}")
    if len(dataf) > numDaysAgo + 1 and len(datag) > numDaysAgo + 1:
        startf = float(dataf[numDaysAgo + 1].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip())
        startg = float(datag[numDaysAgo + 1].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip())
        endf = float(dataf[numDaysAgo + 1 - period].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':','').strip())
        endg = float(datag[numDaysAgo + 1 - period].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':','').strip())
        #for index in reversed(range(numDaysAgo-period, numDaysAgo)):
            #pricef = float(dataf[index].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip())
            #priceg = float(datag[index].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip())
            #if ((startf - pricef)/startf) + ((priceg - startg)/startg) < -.1:

                #return -.1
        val = ((startf - endf)/startf) + ((endg - startg)/startg)
        if val < 100:
            return val
        else:
            return 0
    else:
        return 0

# numDaysAgo refers to the starting date of the month for this return
def getPortfolioMonthlyReturn(listA,listB,numDaysAgo,period):
    totalReturn = 0
    for i in range(0,len(listB)):
        try:
            totalReturn = totalReturn + float(getOneMonthReturn(listA[i],listB[i],numDaysAgo,period))
        except:
            pass
    return totalReturn

listFiles = []
listnames = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.txt"):
    listFiles.append(file)
    listnames.append(file.split("Stocks")[1].split(".")[0].replace("\\", ""))
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.txt"):
    listFiles.append(file)
    listnames.append(file.split("ETFs")[1].split(".")[0].replace("\\", ""))
listClosePrices = []
for file in listFiles:
    f = open(file,"r")
    data = f.read()
    data2 = data.split("}")
    listPrice = []
    for i in range(1, len(data2) - 4):
        listPrice.append(float(data2[i].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip()))
    listClosePrices.append(listPrice)
listReturns = []

for period in range(1,30):
    for startingFactor in reversed(range(1,6)):
        totalReturns = 0
        for counter in range(0,12):
            numDays = 250
            #startingDay = 0
            startingDay = 250*startingFactor - 21*counter
            listNormalizedPrices=[]
            for file in listClosePrices:
                try:
                    if len(file) > startingDay+numDays-1:
                        listclose = []
                        for i in range(startingDay,startingDay+numDays):
                            listclose.append(file[i])
                        listclose.reverse()
                        standardizedlist = [1]
                        for i in range(1,numDays):
                            x = float(listclose[i])
                            y = float(listclose[i - 1])
                            standardizedlist.append(standardizedlist[-1] * x / y)
                        listNormalizedPrices.append(standardizedlist)
                except:
                    print("Exception occurred")
                    pass
            numEquities = len(listNormalizedPrices)
            summarylist = []
            for x in range(0,numEquities-1):
                for y in range(x+1,numEquities):
                    finalswitch = 0
                    totalswitches = 0
                    totaldistance = 0
                    #bollingerx = []
                    #bollingery = []
                    if listNormalizedPrices[x][1] > listNormalizedPrices[y][1]:
                        currentlarger = 0
                    else:
                        currentlarger = 1
                    totaldistance = abs(listNormalizedPrices[x][1] - listNormalizedPrices[y][1])
                    for currentindex in range(2, numDays):
                        totaldistance = totaldistance + abs(float(listNormalizedPrices[x][currentindex])-float(listNormalizedPrices[y][currentindex]))
                        if listNormalizedPrices[x][currentindex] > listNormalizedPrices[y][currentindex]:
                            if currentlarger == 1:
                                totalswitches = totalswitches + 1
                                currentlarger = 0
                                finalswitch = currentindex
                        else:
                            if currentlarger == 0:
                                totalswitches = totalswitches + 1
                                currentlarger = 1
                                finalswitch = currentindex
                    finaldistance = abs(listNormalizedPrices[x][-1]-listNormalizedPrices[y][-1])
                    if listNormalizedPrices[x][-1] > listNormalizedPrices[y][-1]:
                        finalLarger = 0
                    else:
                        finalLarger = 1
                    if totaldistance < 16 and totalswitches > 5 and finalswitch > (numDays*.7) and (.6 > finaldistance > .2):
                        if finalLarger == 0:
                            summarylist.append((listnames[x],listnames[y], totaldistance,finaldistance))
                        else:
                            summarylist.append((listnames[y], listnames[x], totaldistance, finaldistance))

            summarylist.sort(key=itemgetter(3),reverse=True)
            listA = []
            listB = []
            for item in summarylist:
                if item[0] not in listA and item[1] not in listB and len(listB) < 10:
                    listA.append(item[0])
                    listB.append(item[1])
                if len(listB) == 10:
                    break
            monthlyreturn = getPortfolioMonthlyReturn(listA,listB,startingDay,period)
            if monthlyreturn == -1:
                print("Invalid data for this month")
            else:
                totalReturns = totalReturns + monthlyreturn
                print("total: "+str(totalReturns))


        listReturns.append((startingFactor,totalReturns,period))
        print(listReturns)
    print(listReturns)
    try:
        with open('output.txt', 'w') as f:
            f.write(str(listReturns))
    except:
        pass
#xpoints = list(range(1, numDays))
#plt.plot(xpoints, listNormalizedPrices[x])
#plt.plot(xpoints, listNormalizedPrices[y])
#print(summarylist[-1])
#plt.show()

#print(len(distanceList))
#distanceList.sort(key=itemgetter(0))
#distanceList = distanceList[int((len(distanceList)/10)):int(9*(len(distanceList)/10))]
#print(len(distanceList))
#for line in distanceList:
    #print(line)
    #outputstring = outputstring + str(line)+"\n"
#with open('output.txt', 'w') as outfile:
  #  json.dump(outputstring, outfile)
