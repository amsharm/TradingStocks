# import libraries
import numpy as np
import pandas as pd    
# For plotting
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
# Read AUDCAD price series into df data frame
import glob
import csv

listFiles = []
listClosePrices = []
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/Stocks/*.csv"):
    listFiles.append(file)
for file in glob.glob("C:/Users/17132/PycharmProjects/pythonProject/ETFs/*.csv"):
    listFiles.append(file)
for file in listFiles:
    tempList = []
    with open(file, "r") as inputfile:
        csvreader = csv.reader(inputfile)
        header = next(csvreader)
        for row in csvreader:
            try:
                tempList.append(row[0])
            except:
                print("blank: "+str(row[5]))
        if len(tempList) > 0:
            print(tempList[-1])
exit()

df = pd.read_csv('AUDCAD.csv',index_col=0)
# Moving Average
df['moving_average'] = df.prices.rolling(5).mean()  
# Moving Standard Deviation
df['moving_std_dev'] = df.prices.rolling(5).std()
# Compute Upper and lower band
df['upper_band'] = df.moving_average + 0.5*df.moving_std_dev
df['lower_band'] = df.moving_average - 0.5*df.moving_std_dev
# Determine long entry and exit points
df['long_entry'] = df.prices < df.lower_band   
df['long_exit'] = df.prices >= df.moving_average
# Determine short entry and exit points
df['short_entry'] = df.prices > df.upper_band   
df['short_exit'] = df.prices <= df.moving_average
# Consolidate entry and exit into poistions_long and poistions_short
df['positions_long'] = np.nan  
df.loc[df.long_entry,'positions_long']= 1  
df.loc[df.long_exit,'positions_long']= 0    
df['positions_short'] = np.nan  
df.loc[df.short_entry,'positions_short']= -1  
df.loc[df.short_exit,'positions_short']= 0  
# Carry forward poistions
df = df.fillna(method='ffill')
# Consolidate the positions
df['positions'] = df.positions_long + df.positions_short

# Type ypur code below
# Calculate the difference in price
df['prices_difference'] = df.prices - df.prices.shift(1)
# Daily returns
df['daily_returns'] = df.prices_difference / df.prices.shift(1)
# Calculate strategy returns
df['strategy_returns'] = df.daily_returns*df.positions.shift(1)
# Cumulative cumulative strategy returns
df['cumret'] = (df.strategy_returns+1).cumprod()
# Plot the cumulative strategy returns
df.cumret.plot()
plt.show()