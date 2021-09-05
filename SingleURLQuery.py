import requests
import json
import time

symbol = "COST"
url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+str(symbol)+"&outputsize=full&apikey=IRDQSOZCPDU3KH7K"
r = requests.get(url)
data = r.json()
with open('LargestStocks/'+str(symbol)+'.txt', 'w') as outfile:
    json.dump(data, outfile)