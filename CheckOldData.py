import statistics

import requests
import json
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

listFiles = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.txt"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.txt"):
    listFiles.append(file)
for file in listFiles:
    data = open(file,"r").read()
    if data.split("}")[0].__contains__("201") or data.split("}")[0].__contains__("2020"):
        print(file)