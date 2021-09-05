
import requests
import json
import time
import glob

companySymbols = []

for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/LargestStocks/*.txt"):
    companySymbols.append(file.split("\\")[1].split(".")[0])
print(companySymbols)

counter = 0
for symbol in companySymbols:
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&outputsize=full&apikey=3ARTJKXR043OEECM"
    r = requests.get(url)
    data = r.json()
    if str(data).__contains__("Invalid API"):
        print("API call failed for symbol: "+symbol)
    else:
        with open('LargestStocks/'+symbol + '.txt', 'w') as outfile:
            json.dump(data, outfile)

    counter = counter + 1
    print(str(counter) + " "+symbol)
    if counter % 5 == 0:
        time.sleep(60)

