import urllib.request
from datetime import datetime
from datetime import date
import csv

url = "https://api.nomics.com/v1/currencies/ticker?key=f0d696b0a785319e2b1a3b73de96fafa6e259015&ids=BTC,ETH&interval=1h&convert=USD&per-page=100&page=1"
output = str(urllib.request.urlopen(url).read())
btcPrice = output.split("},")[0].split("price")[1].split("price_date")[0].replace("\"","").replace(":","").replace(",","")
ethPrice = output.split("},")[1].split("price")[1].split("price_date")[0].replace("\"","").replace(":","").replace(",","")

now = datetime.now()
today = date.today()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
d3 = today.strftime("%m/%d/%y")
print("d3 =", d3)
btcRow = [d3,current_time,"BTC",btcPrice]
ethRow = [d3,current_time,"ETH",ethPrice]

with open("C:/Users/17132/PycharmProjects/pythonProject/Crypto/BTC.csv", "r") as infile:
    reader = list(csv.reader(infile))
    reader.insert(1, btcRow)

with open("C:/Users/17132/PycharmProjects/pythonProject/Crypto/BTC.csv", "w", newline='') as outfile:
    writer = csv.writer(outfile)
    for line in reader:
        writer.writerow(line)

with open("C:/Users/17132/PycharmProjects/pythonProject/Crypto/ETH.csv", "r") as infile:
    reader = list(csv.reader(infile))
    reader.insert(1, ethRow)

with open("C:/Users/17132/PycharmProjects/pythonProject/Crypto/ETH.csv", "w", newline='') as outfile:
    writer = csv.writer(outfile)
    for line in reader:
        writer.writerow(line)