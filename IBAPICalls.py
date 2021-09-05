import requests
import json
import time
urlValidate = "https://localhost:5000/v1/api/sso/validate"
urlGetTrades = "https://localhost:5000/v1/api/iserver/account/trades"
r = requests.get(urlGetTrades, verify = False)
print(r)