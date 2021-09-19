from rest_framework import serializers
from rest_framework.serializers import Serializer
from PBSTAPP.serializers import CountryExchangeSerializer, CountrySerializer, DailyMatchtrendSerializer, IndexSerializer, SearchSerializer, StockSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ForexTickers, CryptoTickers, IndexTickers, StockTickers, USIndexTicker, USStockTicker
from decouple import config
from requests_cache.session import CachedSession
from .functions import percentagechange, correlationcoefficient, get_client_ip, get_geolocation_for_ip, get_corresponding_currency
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


    # if against == 'usstock':
    #     comp = USStockTicker.objects.all()[:20]
    # elif against == 'crypto':
    #     comp = CryptoTickers.objects.all()[:20]
    # elif against == 'usindex':
    #     comp = USIndexTicker.objects.all()[:20]
    # elif against == 'forex':
    #     comp = ForexTickers.objects.all()[:20]

    # elif against == 'index':
    #     comp = IndexTickers.objects.all()[:20]
    # elif against == 'forex':
    #     comp = StockTickers.objects.all()[:20]

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


@api_view(['GET'])
def Stock_country(request):
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
def Index_country(request):


    data = Search_Country(request, IndexTickers, IndexSerializer)

    return Response(data)

@api_view(['GET'])
def DailyMatchTrend(request):
    Serializer_class = DailyMatchtrendSerializer
    serializer = Serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    days = serializer.data.get('numberOfDays')
    graphValue = serializer.data.get('graphValue')
    pctChange = serializer.data.get('percentageChange')