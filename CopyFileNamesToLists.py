import statistics
import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

fileList = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.txt"):
    fileList.append(file.split("\\")[1].split(".")[0])
with open('SP500List.txt', 'w') as f:
    for item in fileList:
        f.write("%s\n" % item)