from .models import *
from decouple import config
from requests_cache.session import CachedSession
import json
import pandas as pd

tokeniex = config('IEXTOKEN')
token12 = config('TWELVEDATATOKEN')
requests = CachedSession()

# Rapi Api 
headers = {
        'x-rapidapi-key': "72b746e8a4mshac126e6ecc98353p1160c2jsn08be4de1417f",
        'x-rapidapi-host': "twelve-data1.p.rapidapi.com"
        }

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


def correlate_all(symbol, startdate, enddate, hloc, against):
    
    if against == 'stock':
        allStocks = USStockTicker.objects.all()[:20]
    elif against == 'crypto':
        allStocks = cryptolist.objects.all()[:20]
    elif against == 'index':
        allStocks = USIndexTicker.objects.all()[:20]
    elif against == 'forex':
        allStocks = Forexlist.objects.all()[:20]
    
    thelist = []
    for item in allStocks:
        thelist.append(item.symbol)
        
    col =[]

    for items in thelist:
        try:
            col.append(Historic_all_stocks(symbol=items, startdate=startdate, enddate=enddate, HLOC=hloc))
            result = pd.concat(col, axis=1, join='outer')
            
        except KeyError:
            pass
    
    try:
        # final = result.corr()[symbol]
        final = result.corr()

        # finalv2 = final.sort_values(ascending=False)

        # return finalv2.to_dict()
        return final.to_dict()

    except KeyError:
        return "Error"

def correlate_all_stocks(symbol, startdate, enddate, hloc):

    allStocks = USStockTicker.objects.all()[:100]
    
    thelist = []
    for item in allStocks:
        thelist.append(item.symbol)
        
    col =[]

    for items in thelist:
        try:
            col.append(Historic_all_stocks(symbol=items, startdate=startdate, enddate=enddate, HLOC=hloc))
            result = pd.concat(col, axis=1, join='outer')
            
        except KeyError:
            pass
    
    try:
        final = result.corr()[symbol]

        finalv2 = final.sort_values(ascending=False)

        return finalv2.to_dict()

    except KeyError:
        return "Error"

def correlate_all_crypto(symbol, startdate, enddate, hloc):

    allStocks = CryptoTickers.objects.all()[:5]

    thelist = []
    for item in allStocks:
        thelist.append(item.symbol)
        
    col =[]

    for items in thelist:
        try:
            col.append(Historic_all_stocks(symbol=items, startdate=startdate, enddate=enddate, HLOC=hloc))
            result = pd.concat(col, axis=1, join='outer')
            
        except KeyError:
            pass
    
    try:
        final = result.corr()[symbol]

        finalv2 = final.sort_values(ascending=False)

        return finalv2.to_dict()

    except KeyError:
        return "Error"


#ANALYSIS PERFORMED ON HISTORIC DATA
def stockAnalysis(Base_Symbol, Compare_Symbol, startdate, enddate , hloc):
    
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

    # dataList = data['data']

    # index = 0
    # while index < len(dataList):
    #     for key in dataList[index]:
    #         print(dataList[index][key])
    #     index += 1


    # while index < len(dataList):
    #     for items in dataList[index]:
    #         addingtickers = AllStockTickers(
    #                 stockTicker = items['symbol'],
    #                 instrument_name = items['instrument_name'],
    #                 stockExchange = items['exchange'],
    #                 exchange_timezone = items['exchange_timezone'],
    #                 instrument_type = items['instrument_type'],
    #                 stockCountry = items['country'],
    #                 stockCurrency = items['currency']
    #             )
        
    #         addingtickers.save()
    #         index += 1
    #         all_tickers = AllStockTickers.objects.all().order_by('-id')

    #         return all_tickers

def populatingCryptoDB():

    import json

    try:
        url = 'https://api.twelvedata.com/cryptocurrencies'

        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}


    data_list = data['data']

    for items in data_list:

        addingtickers = cryptolist(symbol = items['symbol'])
        addingtickers.save()
        addingtickers.available_exchanges.create(exchanges = items['available_exchanges'])
        addingtickers.currency_base.create(currency_base = items['currency_base'])
        addingtickers.currency_quote.create(currency_quote = items['currency_quote'])

    #     all_tickers = cryptolist.objects.all().order_by('-id')

    # return all_tickers

# def populatingStockDB():

#     import json

#     try:
#         url = 'https://api.twelvedata.com/stocks'

#         data = requests.get(url)

#         if data.status_code == 200:
#             data = json.loads(data.content)

#         else:
#             data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

#     except Exception:
#         data = {'Error':'There has been some connection error. Please try again later.'}


#     data_list = data['data']

#     for items in data_list:

#         addingtickers = stocklist(symbol = items['symbol'], name = items['name'])
#         addingtickers.save()
#         addingtickers.currency.create(currency = items['currency'])
#         addingtickers.exchange.create(exchanges = items['exchange'])
#         addingtickers.country.create(country = items['country'])
#         addingtickers.type.create(type = items['type'])

    #     all_tickers = stocklist.objects.all().order_by('-id')

    # return all_tickers

def populatingForexDB():

    import json

    try:
        url = 'https://api.twelvedata.com/forex_pairs'

        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}


    data_list = data['data']

    for items in data_list:

        addingtickers = Forexlist(symbol = items['symbol'], currency_group = items['currency_group'])
        addingtickers.save()
        addingtickers.currency_base.create(currency_base = items['currency_base'])
        addingtickers.currency_quote.create(currency_quote = items['currency_quote'])

    #     all_tickers = Forexlist.objects.all().order_by('-id')

    # return all_tickers

def populatingIndexDB():

    import json

    try:

        url = 'https://api.twelvedata.com/indices'

        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}


    data_list = data['data']

    for items in data_list:

        addingtickers = IndexList(symbol = items['symbol'], name = items['name'])
        addingtickers.save()
        addingtickers.currency.create(currency = items['currency'])
        addingtickers.country.create(country = items['country'])

    #     all_tickers = stocklist.objects.all().order_by('-id')

    # return all_tickers

# def populatingCommodityDB():

#     import json

#     try:

#         url = 'https://financialmodelingprep.com/api/v3/symbol/available-commodities?apikey=9bd649d08bc15f5c15c45bdcda50ff7b'

#         data = requests.get(url)

#         if data.status_code == 200:
#             data = json.loads(data.content)

#         else:
#             data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

#     except Exception:
#         data = {'Error':'There has been some connection error. Please try again later.'}


#     data_list = data

#     for items in data_list:

#         addingtickers = commoditylist(symbol = items['symbol'], name = items['name'])
#         addingtickers.save()
#         addingtickers.currency.create(currency = items['currency'])
#         addingtickers.stockExchange.create(stockExchange = items['stockExchange'])
#         addingtickers.exchangeShortName.create(exchangeShortName = items['exchangeShortName'])

    #     all_tickers = stocklist.objects.all().order_by('-id')

    # return all_tickers

def dailymatchtrend(symbol):

    try:

        url = f'https://api.twelvedata.com/rocp?symbol={symbol}&interval=1day&include_ohlc=true&apikey={token12}'

        data = requests.get(url)

        if data.status_code == 200:
            # data = json.loads(data.content)
            data = data.json()

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}

    return data

def dailymatchtrendcommodity(symbol):

    try:

        url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?limit=5&apikey=9bd649d08bc15f5c15c45bdcda50ff7b'

        data = requests.get(url)

        if data.status_code == 200:
            # data = json.loads(data.content)
            data = data.json()

        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        data = {'Error':'There has been some connection error. Please try again later.'}

    return data


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