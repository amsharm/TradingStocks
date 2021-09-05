import statistics

import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

listVolume = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.txt"):
    f = open(file,"r")
    data = f.read()
    data2 = data.split("}")
    i = 1
    volume = []
    while (i < 100):
        volume.append(float(data2[i].split("volume")[1].split(",")[0].replace('"', '').replace(':','').strip()))
        i = i + 1
    if statistics.mean(volume) < 2000000:
        listVolume.append((statistics.mean(volume),file.split("Stocks")[1].split(".")[0]))
listVolume.sort(key=itemgetter(1))
for x in listVolume:
    print(x)
print(len(listVolume))