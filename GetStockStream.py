import requests

url = "https://yahoo-finance-low-latency.p.rapidapi.com/v6/finance/quote"

querystring = {"symbols":"AAPL,BTC-USD,EURUSD=X"}

headers = {'x-rapidapi-host': 'yahoo-finance-low-latency.p.rapidapi.com'}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)