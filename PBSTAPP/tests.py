import datetime
from django.test import TestCase
# from datetime import timedelta
# import json

# # Schedule Library imported
# import schedule
import time

# # Create your tests here.
# from requests_cache.session import CachedSession
# requests = CachedSession(expire_after=timedelta(days=1))

# try:
#     url = 'https://api.twelvedata.com/stocks'

#     historic = requests.get(url)

#     if historic.status_code == 200:
#         historic = json.loads(historic.content)


#     else:
#         historic = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

# except Exception:
#     historic = {'Error':'There has been some connection error. Please try again later.'}

# thelist = [1,2,3,4,5,6,7,8,9,12,13,12,14,15,16,17,21,24,54,56,765,876,234,123,1213,1234,35654,6,7657,657,657,65,7,657,8,0,78,5,3,52624,]

# def stuff():
#     print(thelist)

# schedule.every(0.2).seconds.do(stuff)

# i = 0
# while i < 10:
#     schedule.run_pending()
#     time.sleep(1) 

from decouple import config
from requests_cache.session import CachedSession

tokeniex = config('IEXTOKEN')
token12 = config('TWELVEDATATOKEN')
requests = CachedSession()


thelistv = ['aapl', 'btc/eth', 'comp', 'eur/ngn', 'fb', 'amzn', 'goog', 'googl']


def tweleveDataTimeseriesApiCallv2(symbol, output):
    try:

        url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize={output}&apikey={token12}'

        data = requests.get(url)

        if data.status_code == 200:
            # data = json.loads(data.content)
            data = data.json()

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}

    return data

def percentagechangev2(symbol, output, hloc):
    import pandas as pd

    data = tweleveDataTimeseriesApiCallv2(symbol=symbol, output=output)

    data2 = data.get('values')

    thelist = []

    for i in data2:
        thelist.append(float(i[hloc]))

    theseries = pd.Series(thelist)

    result = list(theseries.pct_change())

    result.pop(0)

    rateofchange = []

    for k in result:
        rateofchange.append(k * -100)

    return data, rateofchange

data, pctchange = percentagechangev2('aapl', '7', 'close')

data = data.get('values')

datatime = []
for i in data:
    datatime.append(i['datetime'])

print(
    pctchange[::-1]
)
time.sleep(2)
print(
    datatime
)