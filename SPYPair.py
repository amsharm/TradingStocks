import statistics

import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt

numDays = 100
listnames=[]
listPrices=[]
f = open("C:/Users/17132/PycharmProjects/pythonProject/ETFs/SPY.txt","r")
spydata = f.read()
spydata2 = spydata.split("}")
listspyclose = []
i = 1
while (i < numDays):
    listspyclose.append(spydata2[i].split(":")[5].split(",")[0].replace('"', ''))
    i = i + 1
listspyclose.reverse()

for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.txt"):
    f = open(file,"r")
    data = f.read()
    data2 = data.split("}")
    listclose = []
    listclose.append(file.split("Stocks")[1].split(".")[0])
    i = 1
    print(file)
    while (i < numDays):
        listclose.append(data2[i].split(":")[5].split(",")[0].replace('"', ''))
        i = i + 1
    listclose.reverse()
    listPrices.append(listclose)

for l in listPrices:
    ratiolist = []
    i = 0
    while i < numDays-1:
        ratiolist.append(float(l[i])/float(listspyclose[i]))
        i = i+1
    i = 1
    mean = statistics.mean(ratiolist)
    totaldistance = 0
    totalcrossings = 0
    if ratiolist[0] > mean:
        aboveorbelow = 0
    else:
        aboveorbelow = 1
    while i < numDays-1:
        totaldistance = totaldistance + abs(ratiolist[i] - ratiolist[i-1])
        if ratiolist[i] < mean and aboveorbelow == 0:
            totalcrossings = totalcrossings + 1
            aboveorbelow = 1
        elif ratiolist[i] > mean and aboveorbelow == 1:
            totalcrossings = totalcrossings + 1
            aboveorbelow = 0
        i = i+1
    if totaldistance > .001 and totalcrossings > 0:
        print(l[-1]+" - "+str(totaldistance)+" - "+str(totalcrossings)+" - "+str(mean))
        xpoints = list(range(1, 100))
        plt.plot(xpoints, ratiolist)
        plt.show()

