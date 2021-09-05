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

listFiles = []
listClosePrices = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.txt"):
    listFiles.append(file)
spy = open("C:/Users/17132/PycharmProjects/pythonProject/ETFs/SPY.txt","r").read().split("}")
spyprices = []
masterLength = 60
for file in listFiles:
    filesplit = open(file,"r").read().split("}")
    templist = []
    if len(filesplit) > masterLength:
        for i in range(1,masterLength):
            templist.append(float(filesplit[i].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip()))
            #spyprices.append(float(spy[i].split("adjusted close")[1].split(",")[0].replace('"', '').replace(':', '').strip()))
        templist.reverse()
        listClosePrices.append((templist,file.split("\\")[1].split(".")[0]))
print(len(listClosePrices))
summaryList = []
for x in range(0,len(listClosePrices)-1):
    for y in range(x+1,len(listClosePrices)):
        coeff = (np.coint(listClosePrices[x][0],listClosePrices[y][0])[0,1])
        pctchangeDiffx = (listClosePrices[x][0][masterLength-2]-listClosePrices[x][0][0])/listClosePrices[x][0][0]
        pctchangeDiffy = (listClosePrices[y][0][masterLength-2]-listClosePrices[y][0][0])/listClosePrices[y][0][0]
        pctchangediff = abs(pctchangeDiffx - pctchangeDiffy)
        if pctchangediff > .05:
            if pctchangeDiffx > pctchangeDiffy:
                summaryList.append((coeff,pctchangediff,listClosePrices[x][1],listClosePrices[y][1]))
            else:
                summaryList.append((coeff, pctchangediff, listClosePrices[y][1], listClosePrices[x][1]))
summaryList.sort(key=itemgetter(0),reverse=True)
for item in (summaryList[0:50]):
    print(item)
