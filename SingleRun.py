# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

etf1 = input("Enter first equity")
etf2 = input("Enter second equity")

numDays = 250
file1 = open("C:/Users/17132/PycharmProjects/pythonProject/Stocks/"+etf1+".txt","r")
file2 = open("C:/Users/17132/PycharmProjects/pythonProject/Stocks/"+etf2+".txt","r")
data1 = file1.read()
data2 = file2.read()
splitdata1 = data1.split("}")
splitdata2 = data2.split("}")
listclose1 = []
listclose2 = []
i = 1
while (i < numDays):
    listclose1.append(splitdata1[i].split(":")[5].split(",")[0].replace('"', ''))
    listclose2.append(splitdata2[i].split(":")[5].split(",")[0].replace('"', ''))
    i = i + 1
listclose1.reverse()
listclose2.reverse()
i = 1
standardizedlist1 = [1]
standardizedlist2 = [1]
while i < numDays-1:
    x1 = float(listclose1[i])
    x2 = float(listclose2[i])
    y1 = float(listclose1[i - 1])
    y2 = float(listclose2[i - 1])
    standardizedlist1.append(standardizedlist1[-1] * x1 / y1)
    standardizedlist2.append(standardizedlist2[-1] * x2 / y2)
    i = i + 1

currentindex = 2
finalswitch = 0
totalswitches = 0
totalmaximals = 0
totaldistance = 0
currentdistance = 0
if standardizedlist1[1] > standardizedlist2[1]:
    currentlarger = 0
else:
    currentlarger = 1
currentdistance = abs(standardizedlist1[1] - standardizedlist2[1])
while (currentindex < numDays-1):
    totaldistance = totaldistance + abs(float(standardizedlist1[currentindex])-float(standardizedlist2[currentindex]))
    if standardizedlist1[currentindex] > standardizedlist2[currentindex]:
        if currentlarger == 0:
            if abs(standardizedlist1[currentindex] - standardizedlist2[currentindex]) > currentdistance:
                currentdistance = abs(standardizedlist1[currentindex] - standardizedlist2[currentindex])
        else:
            totalswitches = totalswitches + 1
            totalmaximals = totalmaximals + currentdistance
            currentdistance = abs(standardizedlist1[currentindex] - standardizedlist2[currentindex])
            currentlarger = 0
            finalswitch = currentindex
    else:
        if currentlarger == 1:
            if abs(standardizedlist1[currentindex] - standardizedlist2[currentindex]) > currentdistance:
                currentdistance = abs(standardizedlist1[currentindex] - standardizedlist2[currentindex])
        else:
            totalswitches = totalswitches + 1
            totalmaximals = totalmaximals + currentdistance
            currentdistance = abs(standardizedlist1[currentindex] - standardizedlist2[currentindex])
            currentlarger = 1
            finalswitch = currentindex
    currentindex = currentindex + 1
finaldistance = abs(standardizedlist1[-1]-standardizedlist2[-1])
pastpeak = False
print(str(finalswitch))
print(str(numDays-1))
for index in range(finalswitch,numDays-1):
    print(str(abs(standardizedlist1[index]-standardizedlist2[index])))
    if abs(standardizedlist1[index]-standardizedlist2[index]) > finaldistance:
        pastpeak = True
print("Total distance: "+ str(totaldistance)+" --- Final distance: "+str(abs(standardizedlist1[-1]-standardizedlist2[-1]))+" -- Total switches: "+str(totalswitches) +
                       " - Final switch: " + str(finalswitch) + " -- " + str(pastpeak))

xpoints = list(range(1, numDays))
ypoints = standardizedlist1
plt.plot(xpoints, ypoints)
plt.show()
ypoints = standardizedlist2
plt.plot(xpoints, ypoints)
plt.show()





