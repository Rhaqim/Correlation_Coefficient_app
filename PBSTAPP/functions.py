from .models import *
from decouple import config
from requests_cache.session import CachedSession
import json
import pandas as pd

tokeniex = config('IEXTOKEN')
token12 = config('TWELVEDATATOKEN')
requests = CachedSession()


def tweleveDataTimeseriesApiCall(symbol, startdate, enddate):
    try:

        url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&start_date={startdate}&end_date={enddate}&apikey={token12}'

        data = requests.get(url)

        if data.status_code == 200:
            # data = json.loads(data.content)
            data = data.json()

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}

    return data


# GET VISITOR'S LOCATION FROM IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# GET VISITOR'S LOCATION FROM IP    
def get_geolocation_for_ip(ip):
    api = 'e500e599a5a90d40eea8257b91e35c0a'
    url = f"http://api.ipstack.com/{ip}?access_key={api}"
    response = requests.get(url)
    response.raise_for_status()
    result = response.json()
    return result['country_code'], result['country_name']

# GET CORRESPONDING CURRENCY CODE
def get_corresponding_currency(code):
    country_currency = {
        "BD": "BDT",
        "BE": "EUR",
        "BF": "XOF",
        "BG": "BGN",
        "BA": "BAM",
        "BB": "BBD",
        "WF": "XPF",
        "BL": "EUR",
        "BM": "BMD",
        "BN": "BND",
        "BO": "BOB",
        "BH": "BHD",
        "BI": "BIF",
        "BJ": "XOF",
        "BT": ["BTN", "INR"],
        "JM": "JMD",
        "BV": "NOK",
        "BW": "BWP",
        "WS": "WST",
        "BQ": "USD",
        "BR": "BRL",
        "BS": "BSD",
        "JE": "GBP",
        "BY": "BYR",
        "BZ": "BZD",
        "RU": "RUB",
        "RW": "RWF",
        "RS": "RSD",
        "TL": "USD",
        "RE": "EUR",
        "TM": "TMT",
        "TJ": "TJS",
        "RO": "RON",
        "TK": "NZD",
        "GW": "XOF",
        "GU": "USD",
        "GT": "GTQ",
        "GS": "GBP",
        "GR": "EUR",
        "GQ": "XAF",
        "GP": "EUR",
        "JP": "JPY",
        "GY": "GYD",
        "GG": "GBP",
        "GF": "EUR",
        "GE": "GEL",
        "GD": "XCD",
        "GB": "GBP",
        "GA": "XAF",
        "SV": "USD",
        "GN": "GNF",
        "GM": "GMD",
        "GL": "DKK",
        "GI": "GIP",
        "GH": "GHS",
        "OM": "OMR",
        "TN": "TND",
        "IL": "ILS",
        "JO": "JOD",
        "HR": "HRK",
        "HT": ["HTG", "USD"],
        "HU": "HUF",
        "HK": "HKD",
        "HN": "HNL",
        "HM": "AUD",
        "VE": "VEF",
        "PR": "USD",
        "PS": "ILS",
        "PW": "USD",
        "PT": "EUR",
        "SJ": "NOK",
        "PY": "PYG",
        "IQ": "IQD",
        "PA": ["PAB", "USD"],
        "PF": "XPF",
        "PG": "PGK",
        "PE": "PEN",
        "PK": "PKR",
        "PH": "PHP",
        "PN": "NZD",
        "PL": "PLN",
        "PM": "EUR",
        "ZM": "ZMW",
        "EH": "MAD",
        "EE": "EUR",
        "EG": "EGP",
        "ZA": "ZAR",
        "EC": "USD",
        "IT": "EUR",
        "VN": "VND",
        "SB": "SBD",
        "ET": "ETB",
        "SO": "SOS",
        "ZW": ["USD", "ZAR", "BWP", "GBP", "EUR"],
        "SA": "SAR",
        "ES": "EUR",
        "ER": ["ETB", "ERN"],
        "ME": "EUR",
        "MD": "MDL",
        "MG": "MGA",
        "MF": "EUR",
        "MA": "MAD",
        "MC": "EUR",
        "UZ": "UZS",
        "MM": "MMK",
        "ML": "XOF",
        "MO": "MOP",
        "MN": "MNT",
        "MH": "USD",
        "MK": "MKD",
        "MU": "MUR",
        "MT": "EUR",
        "MW": "MWK",
        "MV": "MVR",
        "MQ": "EUR",
        "MP": "USD",
        "MS": "XCD",
        "MR": "MRO",
        "IM": "GBP",
        "UG": "UGX",
        "MY": "MYR",
        "MX": "MXN",
        "AT": "EUR",
        "FR": "EUR",
        "IO": "USD",
        "SH": "SHP",
        "FI": "EUR",
        "FJ": "FJD",
        "FK": "FKP",
        "FM": "USD",
        "FO": "DKK",
        "NI": "NIO",
        "NL": "EUR",
        "NO": "NOK",
        "NA": ["NAD", "ZAR"],
        "NC": "XPF",
        "NE": "XOF",
        "NF": "AUD",
        "NG": "NGN",
        "NZ": "NZD",
        "NP": "NPR",
        "NR": "AUD",
        "NU": "NZD",
        "CK": "NZD",
        "CI": "XOF",
        "CH": "CHF",
        "CO": "COP",
        "CN": "CNY",
        "CM": "XAF",
        "CL": "CLP",
        "CC": "AUD",
        "CA": "CAD",
        "LB": "LBP",
        "CG": "XAF",
        "CF": "XAF",
        "CD": "CDF",
        "CZ": "CZK",
        "CY": "EUR",
        "CX": "AUD",
        "CR": "CRC",
        "CW": "ANG",
        "CV": "CVE",
        "CU": ["CUP", "CUC"],
        "SZ": "SZL",
        "SY": "SYP",
        "SX": "ANG",
        "KG": "KGS",
        "KE": "KES",
        "SS": "SSP",
        "SR": "SRD",
        "KI": "AUD",
        "KH": "KHR",
        "KN": "XCD",
        "KM": "KMF",
        "ST": "STD",
        "SK": "EUR",
        "KR": "KRW",
        "SI": "EUR",
        "KP": "KPW",
        "KW": "KWD",
        "SN": "XOF",
        "SM": "EUR",
        "SL": "SLL",
        "SC": "SCR",
        "KZ": "KZT",
        "KY": "KYD",
        "SG": "SGD",
        "SE": "SEK",
        "SD": "SDG",
        "DO": "DOP",
        "DM": "XCD",
        "DJ": "DJF",
        "DK": "DKK",
        "VG": "USD",
        "DE": "EUR",
        "YE": "YER",
        "DZ": "DZD",
        "US": "USD",
        "UY": "UYU",
        "YT": "EUR",
        "UM": "USD",
        "TZ": "TZS",
        "LC": "XCD",
        "LA": "LAK",
        "TV": ["TVD", "AUD"],
        "TW": "TWD",
        "TT": "TTD",
        "TR": "TRY",
        "LK": "LKR",
        "LI": "CHF",
        "LV": "EUR",
        "TO": "TOP",
        "LT": "LTL",
        "LU": "EUR",
        "LR": "LRD",
        "LS": ["LSL", "ZAR"],
        "TH": "THB",
        "TF": "EUR",
        "TG": "XOF",
        "TD": "XAF",
        "TC": "USD",
        "LY": "LYD",
        "VA": "EUR",
        "VC": "XCD",
        "AE": "AED",
        "AD": "EUR",
        "AG": "XCD",
        "AF": "AFN",
        "AI": "XCD",
        "VI": "USD",
        "IS": "ISK",
        "IR": "IRR",
        "AM": "AMD",
        "AL": "ALL",
        "AO": "AOA",
        "AN": "ANG",
        "AS": "USD",
        "AR": "ARS",
        "AU": "AUD",
        "VU": "VUV",
        "AW": "AWG",
        "IN": "INR",
        "AX": "EUR",
        "AZ": "AZN",
        "IE": "EUR",
        "ID": "IDR",
        "UA": "UAH",
        "QA": "QAR",
        "MZ": "MZN"
    }

    for key, value in country_currency.items():
        if key == code:
            return value


####################################################################################################

# SEARCH SINGLE STOCK
# baseurl = 'https://cloud.iexapis.com/stable/stock/'
# stockticker = 'aapl'

def search_stock_ticker(base_url, stock_ticker):
    try:
        token = tokeniex

        url = base_url + stock_ticker + '/quote?token=' + token

        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}

    return data


#SEARCH BATCH STOCK
# batchbaseurl = 'https://cloud.iexapis.com/stable/stock/market/batch?symbols='
# stocktickers = 'aapl,goog'

def search_stock_batch(base_url, stock_tickers):
    data_list = []

    try:
        token = tokeniex
        url = base_url + stock_tickers + '&types=quote&token=' + token
        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)
            for item in data:
                data_list.append(data[item]['quote'])
        else:
            data = {'Error' : 'There has been an unexpected issues. Please try again'}
    except Exception as e:
        data = {'Error':'There has been some connection error. Please try again later.'}
    return data_list



# CHECKING VALID STOCK TICKER
def check_valid_stock_ticker(stock_ticker):
    base_url = 'https://cloud.iexapis.com/stable/stock/'
    stock = search_stock_ticker(base_url, stock_ticker)
    if 'Error' in stock:
        return False
    else:
        return True


# CHECKING IF STOCK IN PORTFOLIO ALREADY
# def check_stock_ticker_existed(stock_ticker):

#     if Stock.objects.filter(stock_ticker=stock_ticker).exists():
#         return True
#     else:
#         return False

#     # try:
#     #     stock = Stock.objects.get(stock_ticker=stock_ticker)
#     #     if stock:
#     #         return True
#     # except Exception:
#     #     return False

# def check_crypto_ticker_existed(crypto_ticker):

#     if Crypto.objects.filter(stock_ticker=crypto_ticker).exists():
#         return True
#     else:
#         return False



#UPDATING STOCK QUOTE DAILY, MIGHT NOT BE NECESSARY ANYMORE
# def StockQuote(symbol):
#     import datetime 

#     try:

#         url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote&range=1w&token={tokeniex}'

#         iexdataquote = requests.get(url)

#         if iexdataquote.status_code == 200:
#             iexdataquote = json.loads(iexdataquote.content)

#         else:
#             iexdataquote = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

#     except Exception:
#         iexdataquote = {'Error':'There has been some connection error. Please try again later.'}

#     for itemz in iexdataquote.values():

#         for i in itemz.values():
            
#             dailystockquote = StockQuoteDaily(

#                 stockname = i['companyName'],
#                 stocksymbol = i['symbol'],
#                 stockexchange = i['primaryExchange'],
#                 stockcurrency = i['currency'],

#                 stockopen = i['open'],
#                 stockclose = i['close'],
#                 stockhigh = i['high'],
#                 stocklow = i['low'],
#                 stockvolume = i['latestVolume'],

#                 previousclose = i['previousClose'],
#                 percentagechange = i['changePercent'],
#                 ytdchange = i['ytdChange'],
#                 marketcap = i['marketCap'],
#                 peratio = i['peRatio'],
#                 week52high = i['week52High'],
#                 week52low = i['week52Low'],
#                 updateTime =  datetime.datetime.fromtimestamp(i['lastTradeTime'] // 1000).strftime('%Y-%m-%d')
#                     )
#             dailystockquote.save()

#             retrievedDailyQuote = StockQuoteDaily.objects.all().order_by('-id')

#             return retrievedDailyQuote


#GETTING HISTORIC DATA TO BE USED FOR ANALYSIS
def Historic(symbol, startdate, enddate, HLOC='low'):

    try:
        url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&start_date={startdate}&end_date={enddate}&apikey={token12}'

        historic = requests.get(url)

        if historic.status_code == 200:
            historic = json.loads(historic.content)


        else:
            historic = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        historic = {'Error':'There has been some connection error. Please try again later.'}
    
    values = ''
    if historic['status'] != 'error':
        values =  historic['values']

    open = []
    for value in values:
        open.append(value[HLOC])

    final = [float(i) for i in open]
    return final

#CORRELATING ALL STOCKS WITH EACHOTHER
def Historic_all_stocks(symbol, startdate, enddate, HLOC='close'):

    try:
        url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&start_date={startdate}&end_date={enddate}&apikey={token12}'

        historic = requests.get(url)

        if historic.status_code == 200:
            historic = json.loads(historic.content)
        elif historic.status_code == 400:
            pass
        else:
            pass
            historic = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        pass
        historic = {'Error':'There has been some connection error. Please try again later.'}

    values =  historic['values']

    open = []
    for value in values:
        open.append(value[HLOC])

    final = [float(i) for i in open]

    check = {symbol:final}
    return pd.DataFrame(check)


#ANALYSIS PERFORMED ON HISTORIC DATA
def correlationcoefficient(Base_Symbol, Compare_Symbol, startdate, enddate , hloc):
    
    from statistics import mean
    from math import sqrt

    Base_Symbol = Historic(Base_Symbol, startdate=startdate, enddate=enddate, HLOC=hloc)
    Compare_Symbol = Historic(Compare_Symbol, startdate=startdate, enddate=enddate, HLOC=hloc)

    Base_Symbolsqrd = [a * b for a, b in zip(Base_Symbol, Base_Symbol)]
    Compare_Symbolsqrd = [a * b for a, b in zip(Compare_Symbol, Compare_Symbol)]
    multiplys1s2 = [a * b for a, b in zip(Base_Symbol, Compare_Symbol)]

    meanBase_Symbol = mean(Base_Symbol)
    meanCompare_Symbol = mean(Compare_Symbol)

    meanBase_Symbolsqrd = mean(Base_Symbolsqrd)
    meanCompare_Symbolsqrd = mean(Compare_Symbolsqrd)
    meanmult = mean(multiplys1s2)

    varianceBase_Symbol = meanBase_Symbolsqrd - meanBase_Symbol * meanBase_Symbol
    varianceCompare_Symbol = meanCompare_Symbolsqrd - meanCompare_Symbol * meanCompare_Symbol

    covariance = meanmult - meanBase_Symbol * meanCompare_Symbol

    corrcoefficient = covariance / sqrt(varianceBase_Symbol * varianceCompare_Symbol)

    return corrcoefficient

def getcorr(base_ticker, compare_tickers, startDate, endDate , graphValue):
    res = {}

    stv = []

    # col = []

    # for stuff in compare_tickers:
    #     try:
    #         stv2 = correlationcoefficient(Base_Symbol=base_ticker, Compare_Symbol=stuff, startdate=startDate, enddate=endDate, hloc=graphValue)
    #         col.append({stuff:stv2})
    #     except:
    #         pass

    for stuff in compare_tickers:
        try:
            stv.append(correlationcoefficient(Base_Symbol=base_ticker, Compare_Symbol=stuff, startdate=startDate, enddate=endDate, hloc=graphValue))
            for i in stv:
                res[stuff] = i #convert into a dictionary
                stv.remove(i)
                break
        except:
            pass
    
    ans = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)} #sort list in ascendinf order

    return ans

def stockAnalysisV1(Base_Symbol, startdate, enddate, hloc):
    
    from statistics import mean
    from math import sqrt

    Base_Symbol = Historic(Base_Symbol, startdate=startdate, enddate=enddate , HLOC=hloc)

    allStocks = USStockTicker.objects.all()[:5]

    thelist = []
    for item in allStocks:
        thelist.append(item.symbol)
        
    # col =[]

    for items in thelist:
        try:
            Compare_Symbol = Historic(symbol=items, startdate=startdate, enddate=enddate , HLOC=hloc)
            # result = pd.concat(col, axis=1, join='outer')
            
        except KeyError:
            pass


    # Compare_Symbol = Historic(Base_Symbol, startdate=startdate, enddate=enddate , HLOC=hloc)

    Base_Symbolsqrd = [a * b for a, b in zip(Base_Symbol, Base_Symbol)]
    Compare_Symbolsqrd = [a * b for a, b in zip(Compare_Symbol, Compare_Symbol)]
    multiplys1s2 = [a * b for a, b in zip(Base_Symbol, Compare_Symbol)]

    meanBase_Symbol = mean(Base_Symbol)
    meanCompare_Symbol = mean(Compare_Symbol)

    meanBase_Symbolsqrd = mean(Base_Symbolsqrd)
    meanCompare_Symbolsqrd = mean(Compare_Symbolsqrd)
    meanmult = mean(multiplys1s2)

    varianceBase_Symbol = meanBase_Symbolsqrd - meanBase_Symbol * meanBase_Symbol
    varianceCompare_Symbol = meanCompare_Symbolsqrd - meanCompare_Symbol * meanCompare_Symbol

    covariance = meanmult - meanBase_Symbol * meanCompare_Symbol

    corrcoefficient = covariance / sqrt(varianceBase_Symbol * varianceCompare_Symbol)

    return corrcoefficient

##FUNCTION TO POPULATE DATABASE ##DO NOT CALL UNLESS TO UPDATE DATABASE
def populatingDB():

    import json

    try:

        url = 'https://api.twelvedata.com/stocks'
        # url = 'https://api.twelvedata.com/cryptocurrencies'
        # url = 'https://api.twelvedata.com/forex_pairs'
        # url = 'https://api.twelvedata.com/indices?country=us'

        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}


    data_list = data['data']

    # obj_list = [USIndexTicker(**data_dict) for data_dict in data_list]
    # objs = USIndexTicker.objects.bulk_create(obj_list)

    # obj_list = [USStockTicker(**data_dict) for data_dict in data_list]
    # objs = USStockTicker.objects.bulk_create(obj_list)

    # #FOR STOCK 
    obj_list = [StockTickers(**data_dict) for data_dict in data_list]
    objs = StockTickers.objects.bulk_create(obj_list)

    # #FOR CRYPTO
    # obj_list = [CryptoTickers(**data_dict) for data_dict in data_list]
    # objs = CryptoTickers.objects.bulk_create(obj_list)

    # #FOR FOREX
    # obj_list = [ForexTickers(**data_dict) for data_dict in data_list]
    # objs = ForexTickers.objects.bulk_create(obj_list)

    # #FOR INDEX
    # obj_list = [IndexTickers(**data_dict) for data_dict in data_list]
    # objs = IndexTickers.objects.bulk_create(obj_list)

    return objs

def percentagechange(symbol, startdate, enddate, hloc):
    import pandas as pd

    data = tweleveDataTimeseriesApiCall(symbol=symbol, startdate=startdate, enddate=enddate)

    data2 = data.get('values')

    thelist = []

    for i in data2:
        thelist.append(float(i[hloc]))

    theseries = pd.Series(thelist)

    result = list(theseries.pct_change())

    return data, result


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

def percentagechangev2(symbol, output, hloc, pctChange):
    import pandas as pd

    data = tweleveDataTimeseriesApiCallv2(symbol=symbol, output=output) #external api with outputsize instead of date

    data2 = data.get('values')

    thelist = []

    for i in data2:
        thelist.append(float(i[hloc])) #get values for HLOC

    theseries = pd.Series(thelist[::-1])

    result = list(theseries.pct_change()) #pandas percentage change

    result.pop(0) #remove nan value

    rateofchange = []

    for k in result:
        rateofchange.append(k * 100) #per client request multiply by 100, result negative hence -100 multiplication

    percentage_ = pctChange / 100

    discount = []

    for i in rateofchange:
        discount.append(float(i) * float(percentage_))

    postiveChange = [x + y for x, y in zip(rateofchange, discount)]

    negativeChange = [x - y for x, y in zip(rateofchange, discount)]

    return data2, postiveChange, negativeChange


def actualValuechangev2(symbol, output, hloc, pctChange):

    data = tweleveDataTimeseriesApiCallv2(symbol=symbol, output=output) #external api with outputsize instead of date

    data2 = data.get('values')

    thelist = []

    for i in data2:
        thelist.append(float(i[hloc])) #get values for HLOC

    thelist = thelist[::-1]


    percentage_ = pctChange / 100

    discount = []

    for i in thelist:
        discount.append(float(i) * float(percentage_))

    postiveChange = [x + y for x, y in zip(thelist, discount)]

    negativeChange = [x - y for x, y in zip(thelist, discount)]

    return data2, postiveChange, negativeChange

# def changeResults(symbol, start, end, hloc, days):
#     import yfinance as yf


#     ticker = yf.Ticker(symbol)

#     historical = ticker.history(period="max")

#     data = historical[hloc]

#     offset = days + 7

# def validate(value, merger):
#     is_between = []
#     for r in merger:
#         if r[0] <= value <= r[1]:
#             is_between.append(value)
#         else:
#             pass

#     return is_between


def changeResultsv2(symbol, start, stop, hloc):

    try:

        url = f'https://cloud.iexapis.com/stable/stock/{symbol}/chart/max?token={tokeniex}'

        data = requests.get(url)

        if data.status_code == 200:
            # data = json.loads(data.content)
            data = data.json()

        else:
            data = data.status_code

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}

    values = []

    date = []

    for items in data:
        values.append(items[hloc])
        date.append(items['date'])

    check_value = values[::-1]
    check_date = date[::-1]

    merge = [[x]+[y] for x, y in zip(start, stop)]

    enum_merge = list(enumerate(merge))

    item = len(check_value)

    results = []

    for i in range(item):
        first = check_value[i]
        second = check_value[i + 1]
        third = check_value[i + 2]
        if enum_merge[0][1][0] < first < enum_merge[0][1][1] and enum_merge[1][1][0] < second < enum_merge[1][1][1] and enum_merge[2][1][0] < third < enum_merge[2][1][1]:
            # print(check_date[i], first)
            # print(check_date[i + 1], second)
            # print(check_date[i + 2], third)
            results.append([check_date[i], first, check_date[i + 1], second], check_date[i + 2], third)
        elif IndexError:
            pass

    return results

def PowerRegressPrediction(symbol, hloc, power:int, startdate, enddate):
    import datetime as dt
    import numpy as np

    data = tweleveDataTimeseriesApiCall(symbol, startdate, enddate)

    ticker = data.get('values')

    historical = {}

    dates = []

    targets = []

    for items in ticker:

        dates.append(items["datetime"])

        targets.append(items[hloc])

    final_dates = pd.Series(dates)
    final_targets = pd.Series(targets)

    historical["Date"] = pd.to_datetime(final_dates)

    historical["Date"] = historical["Date"].map(dt.datetime.toordinal)

    historical["target"] = pd.to_numeric(final_targets)

    X = np.array(historical["Date"])
    Y = np.array(historical["target"])

    check = np.polyfit(X, Y, power)

    correlation = np.corrcoef(X, Y)[0,1]

    r2 = correlation**2
 
    p = np.poly1d(check)

    return check, r2, p