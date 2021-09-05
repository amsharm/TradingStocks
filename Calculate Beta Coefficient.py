import yahoo_fin.stock_info as si
import glob

outList = []

tickerList = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    tickerList.append(file.split("\\")[1].split(".")[0])
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    tickerList.append(file.split("\\")[1].split(".")[0])
counter = 0
for item in tickerList:
    counter = counter + 1
    print(counter)
    print(item)
    try:
        quote_table = si.get_quote_table(item, dict_result=False)
        outList.append((item,str(quote_table).splitlines()[5].split(")")[1].strip()))
    except:
        pass
for item in outList:
    print(item)