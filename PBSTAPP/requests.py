from PBSTAPP.models import ForexTickers, CryptoTickers, IndexTickers, StockTickers, USIndexTicker, USStockTicker
from decouple import config
from requests_cache.session import CachedSession
import time
import schedule

requests = CachedSession()
token12 = config('TWELVEDATATOKEN')
tokeniex = config('IEXTOKEN')


comp = USStockTicker.objects.all()


thelist = []
for item in comp:
    thelist.append(item.symbol)


def dailyrequest(symbol):
    try:

        url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&apikey={token12}'

        data = requests.get(url)

        if data.status_code == 200:
            # data = json.loads(data.content)
            data = data.json()

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}

    return data

def stuff():
    for symbol in thelist:
        dailyrequest(symbol)
        time.sleep(0.5)
    
schedule.every(24).hours.do(stuff)


while True:
    schedule.run_pending()
    time.sleep(1)
