from PBSTAPP.serializers import BasePredSerializer, CorrelationSerializer, CountryExchangeSerializer, CountrySerializer, DailyMatchtrendSerializer, ExchangeSerializer, IndexSerializer, SearchSerializer, StockSerializer, PowerPredSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ForexTickers, CryptoTickers, IndexTickers, StockTickers, USStockTicker
from decouple import config
from requests_cache.session import CachedSession
from .functions import actualValuechangev2, percentagechange, correlationcoefficient, get_client_ip, get_geolocation_for_ip, get_corresponding_currency, percentagechangev2, getcorr, PowerRegressPrediction, ExponRegressPrediction, polyPredictions
import json

requests = CachedSession()
token12 = config('TWELVEDATATOKEN')
tokeniex = config('IEXTOKEN')

@api_view(['GET'])
def Homepage(request):
    

    context = "serializer_model.data"

    return Response(context)



#General function 
def generalPurpose(request, against):
    serializer_class = SearchSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    symbolValue = serializer.data.get('symbolValue')
    startDate = serializer.data.get('startdate')
    endDate = serializer.data.get('enddate')
    hloc = serializer.data.get('hloc')

    datatrend, pctchange = percentagechange(symbol=symbolValue, startdate=startDate, enddate=endDate, hloc=hloc)

    pctchange.pop(0)

    checking = datatrend['values']

    datetimelist = []

    for i in checking:
        datetimelist.append(i['datetime'])
    
    rateofchange = []

    for k in pctchange:
        rateofchange.append(k * -100)

    res = {}

    for key in datetimelist:
        for value in rateofchange:
            res[key] = value
            rateofchange.remove(value)
            break 

    comp = against

    col = []
    thelist = []
    for item in comp:
        thelist.append(item.symbol)

    for stuff in thelist:
        try:
            stv2 = correlationcoefficient(Base_Symbol=symbolValue, Compare_Symbol=stuff, startdate=startDate, enddate=endDate, hloc=hloc)
            col.append({stuff:stv2})
        except:
            pass

    context = {
        # 'DMT': datatrend['values'],
        'coefficient': col,
        # 'pctchange': res
    }

    return context


@api_view(['GET'])
def forexV2(request):

    context = generalPurpose(request, ForexTickers.objects.all()[:20])

    return Response(context)

@api_view(['GET'])
def cryptoV2(request):

    context = generalPurpose(request, CryptoTickers.objects.all()[:20])

    return Response(context)

@api_view(['GET'])
def indexV2(request):

    context = generalPurpose(request, IndexTickers.objects.all()[:20])

    return Response(context)

@api_view(['GET'])
def stockV2(request):

    context = generalPurpose(request, USStockTicker.objects.all()[14000:14100])

    return Response(context)

#Homepage
@api_view(['GET'])
def forexhomepage(request):

    ip = get_client_ip(request)

    country_code, country_name = get_geolocation_for_ip(ip)

    country_code = get_corresponding_currency(country_code)

    country_code = "ngn"

    try:

        url = f"https://api.twelvedata.com/price?symbol=USD/{country_code}&apikey={token12}"

        visitorscurrency = requests.get(url)

        if visitorscurrency.status_code == 200:
            visitorscurrency = json.loads(visitorscurrency.content)

        else:
            visitorscurrency = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}

    except Exception:
        visitorscurrency = {'Error':'There has been some connection error. Please try again later.'}

    context = {
        'visitorscurrency': visitorscurrency,
        'country_name': country_name,
        'country_code': country_code,
    }

    return Response(context)


def Search_Country(request, model, serializer_model):
    serializer_class = CountrySerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    country = serializer.data.get('country')

    QuerySet = model.objects.all().filter(country__icontains= country)

    serialized_model = serializer_model(QuerySet, many=True)

    context = serialized_model.data

    return context

def Search_exchange(request, model, serializer_model):
    serializer_class = ExchangeSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    excahnge = serializer.data.get('exchange')

    QuerySet = model.objects.all().filter(exchange__icontains= excahnge)

    serialized_model = serializer_model(QuerySet, many=True)

    context = serialized_model.data

    return context


@api_view(['GET'])
def Stock_search(request):
    serializer_class = CountryExchangeSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    country = serializer.data.get('country')
    exchange = serializer.data.get('exchange')

    QuerySet = StockTickers.objects.all().filter(country__icontains= country)

    if exchange != None:
        QuerySet = QuerySet.filter(exchange__icontains = exchange)

    serializer_model = StockSerializer(QuerySet, many=True)

    context = serializer_model.data

    return Response(context)


@api_view(['GET'])
def Index_search(request):
    serializer_class = CountryExchangeSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    country = serializer.data.get('country')
    # exchange = serializer.data.get('exchange')

    QuerySet = IndexTickers.objects.all().filter(country__icontains= country)

    # if exchange != None:
    #     QuerySet = QuerySet.filter(exchange__icontains = exchange)

    serializer_model = IndexSerializer(QuerySet, many=True)

    context = serializer_model.data

    return Response(context)


#FEATURES

#CORRELATION
@api_view(['GET', 'POST'])
def Correlation(request):
    serializer_class = CorrelationSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    base_ticker = serializer.data.get('base_ticker')
    compare_tickers = serializer.data.get('compare_tickers')
    startDate = serializer.data.get('startDate')
    endDate = serializer.data.get('endDate')
    graphValue = serializer.data.get('graphValue')

    ans = getcorr(base_ticker, compare_tickers, startDate, endDate , graphValue)

    context = {
        "correlation":ans
    }

    return Response(context)

#DAILY MATCH TREND
@api_view(['GET', 'POST'])
def DailyMatchTrend(request):
    Serializer_class = DailyMatchtrendSerializer
    serializer = Serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    ticker = serializer.data.get('ticker')
    days = serializer.data.get('numberOfDays')
    graphValue = serializer.data.get('graphValue')
    pctChange = serializer.data.get('percentageChange')
    change_choice = serializer.data.get('change_choice')

    if change_choice == 'actChange':
        date, postiveChange, negativeChange = actualValuechangev2(ticker, days, graphValue, pctChange)
    
    if change_choice == 'pctChange':
        date, postiveChange, negativeChange = percentagechangev2(ticker, days, graphValue, pctChange)
    

    context = {
        'positive': postiveChange[::-1],
        'negative': negativeChange[::-1],
        'date':date,
    }

    return Response(context)

# Predictions
@api_view(['GET', 'POST'])
def predictions(request):
    Serializer_class = PowerPredSerializer
    serializer = Serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    ticker = serializer.data.get('ticker')
    startDate = serializer.data.get('startDate')
    endDate = serializer.data.get('endDate')
    graphValue = serializer.data.get('graphValue')
    power = serializer.data.get('power')

    # results, poly_formula, ticker_date, ticker_target = PowerRegressPrediction(ticker, graphValue, power, startDate, endDate)
    results, poly_formula, ticker_date = PowerRegressPrediction(ticker, graphValue, power, startDate, endDate)

    str_poly = str(poly_formula)

    context = {
        'formula_data':results,
        'str_form':str_poly,
        'ticker_date':ticker_date,
        # 'ticker_target':ticker_target,
    }

    return Response(context)

@api_view(['GET', 'POST'])
def ExponPrediction(request):
    Serializer_class = BasePredSerializer
    serializer = Serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    ticker = serializer.data.get('ticker')
    startDate = serializer.data.get('startDate')
    endDate = serializer.data.get('endDate')
    graphValue = serializer.data.get('graphValue')

    formula_data, r_squared, ticker_date, ticker_target = ExponRegressPrediction(ticker, graphValue, startDate, endDate)

    context = {
        'formula_data':formula_data,
        'r_squared':r_squared,
        'ticker_date':ticker_date,
        'ticker_target':ticker_target,
    }

    return Response(context)

@api_view(['GET', 'POST'])
def PolyPredictions(request):
    Serializer_class = PowerPredSerializer
    serializer = Serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    ticker = serializer.data.get('ticker')
    startDate = serializer.data.get('startDate')
    endDate = serializer.data.get('endDate')
    graphValue = serializer.data.get('graphValue')
    power = serializer.data.get('power')

    formula_data, r_squared, ticker_date, ticker_target = polyPredictions(ticker, graphValue, startDate, endDate, power)

    context = {
        'formula_data':formula_data,
        'r_squared':r_squared,
        'ticker_date':ticker_date,
        'ticker_target':ticker_target,
    }

    return Response(context)