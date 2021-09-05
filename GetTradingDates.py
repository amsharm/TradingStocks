import datetime as dt
from datetime import timedelta

def getDates(numDays):
    holidays2021 = ["2021-01-01","2021-01-18","2021-02-15","2021-04-02","2021-05-31","2021-07-05","2021-09-06","2021-11-25","2021-12-24"]
    holidays2020 = ["2020-01-01","2020-01-20","2020-02-17","2020-04-10","2020-05-25","2020-07-03","2020-09-07","2020-11-26","2020-12-25"]
    holidays2019 = ["2019-01-01","2019-01-21","2019-02-18","2019-04-19","2019-05-27","2019-07-04","2019-09-02","2019-11-28","2019-12-25"]
    holidays2018 = ["2018-01-01","2018-01-15","2018-02-19","2018-03-30","2018-05-28","2018-07-04","2018-09-03","2018-11-22","2018-12-25"]
    holidays2017 = ["2017-01-01","2017-01-16","2017-02-20","2017-04-14","2017-05-29","2017-07-04","2017-09-04","2017-11-23","2017-12-25"]
    holidays2016 = ["2016-01-01","2016-01-18","2016-02-15","2016-03-25","2016-05-30","2016-07-04","2016-09-05","2016-11-24","2016-12-26"]
    listDates = []
    timediff = 0
    while len(listDates) < numDays:
        date = dt.date.today() - timedelta(days=timediff)
        if 0 <= date.weekday() < 5 and str(date) not in holidays2021 and str(date) not in holidays2020 and str(date) not in holidays2016 and str(date) not in holidays2019 and str(date) not in holidays2017 and str(date) not in holidays2018:
            listDates.append(date)
        timediff = timediff + 1
    return listDates
