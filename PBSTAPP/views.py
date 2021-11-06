from rest_framework.fields import set_value
from PBSTAPP.serializers import BasePredSerializer, CorrelationSerializer, CountryExchangeSerializer, CountrySerializer, CryptoSerializer, DailyMatchtrendSerializer, ExchangeSerializer, ForexSerializer, IndexSerializer, SearchSerializer, StockSerializer, PowerPredSerializer, NameSearchSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ForexTickers, CryptoTickers, IndexTickers, StockTickers, USStockTicker
from django.db.models import Q
from decouple import config
from requests_cache.session import CachedSession
from .functions import LogPredictions, PCTdailyMatchTrendSearch, actualValuechangev2, dailyMatchTrendSearch, percentagechange, correlationcoefficient, get_client_ip, get_geolocation_for_ip, get_corresponding_currency, percentagechangev2, getcorr, PowerRegressPrediction, ExponRegressPrediction, polyPredictions
import json

requests = CachedSession()
token12 = config('TWELVEDATATOKEN')
tokeniex = config('IEXTOKEN')

@api_view(['GET'])
def Homepage(request):
    
    serializer_model = StockSerializer(many=True)

    context = serializer_model.data
    # context = "serializer_model.data"

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

#DATABASE QUERY FUNCTIONS
@api_view(['GET'])
def Search_all_stock(request):
    # serializer_class = NameSearchSerializer
    # serializer = serializer_class(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # name_query = serializer.data.get('name')

    if request.method == "GET":

        name_query = request.GET.get('name', None)
        country_query = request.GET.get('country', None)
        exchange_query = request.GET.get('exchange', None)

        # ticker_names = (StockTickers.objects
        #                 .filter(symbol__startswith=name_query)
        #                 .values_list('symbol', 'name', 'exchange', 'country'))

        if country_query != None:
            country = (StockTickers.objects.all().filter(Q(country__icontains=country_query)))

            ticker_names = (country.filter(Q(symbol__istartswith=name_query) | Q(name__istartswith=name_query)))

            if exchange_query != None:
                exchange = (country.filter(Q(exchange__istartswith=exchange_query)))

                ticker_names = (exchange.filter(Q(symbol__istartswith=name_query) | Q(name__istartswith=name_query)))

        elif exchange_query != None:
            exchange = (StockTickers.objects.all().filter(Q(exchange__icontains=exchange_query)))

            ticker_names = (exchange.filter(Q(symbol__istartswith=name_query) | Q(name__istartswith=name_query)))

            if country_query != None:
                country = (exchange.filter(Q(country__istartswith=country_query)))

                ticker_names = (country.filter(Q(symbol__istartswith=name_query) | Q(name__istartswith=name_query)))

        else:
            ticker_names = (StockTickers.objects.all().filter(Q(symbol__istartswith=name_query) | Q(name__istartswith=name_query)))

        serializer_model = StockSerializer(ticker_names, many=True)

        return Response(serializer_model.data)

@api_view(['GET'])
def Search_all_forex(request):
    # serializer_class = NameSearchSerializer
    # serializer = serializer_class(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # name_query = serializer.data.get('name')

    if request.method == "GET":

        name_query = request.GET.get('name')

    # ticker_names = (ForexTickers.objects
    #                 .filter(symbol__startswith=name_query)
    #                 .values_list('symbol', flat=True))

        ticker_names = (ForexTickers.objects.all().filter(Q(symbol__icontains=name_query) | Q(currency_quote__icontains=name_query) | Q(currency_base__icontains=name_query)))

        serializer_model = ForexSerializer(ticker_names, many=True)

        return Response(serializer_model.data)

@api_view(['GET'])
def Search_all_crypto(request):
    # serializer_class = NameSearchSerializer
    # serializer = serializer_class(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # name_query = serializer.data.get('name')

    if request.method == "GET":

        name_query = request.GET.get('name')

    # ticker_names = (CryptoTickers.objects
    #                 .filter(symbol__startswith=name_query)
    #                 .values_list('symbol', flat=True))

        ticker_names = (CryptoTickers.objects.all().filter(Q(symbol__icontains=name_query) | Q(currency_quote__icontains=name_query) | Q(currency_base__icontains=name_query)))

        serializer_model = CryptoSerializer(ticker_names, many=True)

        return Response(serializer_model.data)

@api_view(['GET'])
def search_exchanges(request):
    if request.method == "GET":

        country_query = request.GET.get('country', None)

        # ticker_names = (StockTickers.objects
        #                 .filter(symbol__startswith=name_query)
        #                 .values_list('symbol', 'name', 'exchange', 'country'))

        query_values = (StockTickers.objects.all().filter(Q(country__icontains=country_query)).values_list('exchange'))

        inter_m = set(query_values)

        exchanges = list(inter_m)

        return Response(exchanges)



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
    # if request.method == "GET":
    #     base_ticker = request.GET.get('base_ticker')
    #     compare_tickers = request.GET.get('compare_tickers')
    #     startDate = request.GET.get('startDate')
    #     endDate = request.GET.get('endDate')
    #     graphValue = request.GET.get('graphValue')

    ans, positivelyCorrelated, negativelyCorrelated = getcorr(base_ticker, compare_tickers, startDate, endDate , graphValue)

    context = {
        "correlation":ans,
        "positivelyCorrelated":positivelyCorrelated,
        "negativelyCorrelated":negativelyCorrelated,
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

    # if request.method == "GET":

    #     ticker = request.GET.get('ticker')
    #     days = request.GET.get('numberOfDays')
    #     graphValue = request.GET.get('graphValue')
    #     pctChange = request.GET.get('percentageChange')
    #     change_choice = request.GET.get('change_choice')

    if change_choice == 'actChange':
        date, postiveChange, negativeChange = actualValuechangev2(ticker, int(days), graphValue, int(pctChange))
        
        try:
            DMT_values, DMT_dates = dailyMatchTrendSearch(ticker, negativeChange, postiveChange, graphValue)
        
        except IndexError:
            DMT_values, DMT_dates = "Try a smaller number of days or a different Percentgae Change", "Try a smaller number of days or a different Percentgae Change"

    if change_choice == 'pctChange':
        days = days + 1
        date, postiveChange, negativeChange = percentagechangev2(ticker, int(days), graphValue, int(pctChange))
        date.pop()
        
        try:
            DMT_values, DMT_dates = PCTdailyMatchTrendSearch(ticker, negativeChange, postiveChange, graphValue)
        
        except IndexError:
            DMT_values, DMT_dates = "Try a smaller number of days or a different Percentgae Change", "Try a smaller number of days or a different Percentgae Change"

    positive_ = postiveChange[::-1]
    negative_ = negativeChange[::-1]

    datetime = []
    hloc_values = []

    for items in date:
        datetime.append(items['datetime'])
        hloc_values.append(items[graphValue])

    for dates in datetime:
        for i in range(len(datetime)):
            if i == 0:
                main_array = [{'date':dates, 'hloc_values':hloc_values[i], 'positive':positive_[i], 'negative':negative_[i]}]
            else:
                main_array.append({'date':dates, 'hloc_values':hloc_values[i], 'positive':positive_[i], 'negative':negative_[i]})
    
    values = []
    ddates = []

    for i, j in DMT_dates.items():
        ddates.append(j)

    for l, m in DMT_values.items():
        values.append(m)

    for i in range(len(ddates)):
        if i == 0:
            dmt_array = [{'DMTdate':ddates[i], 'DMTvalues':values[i]}]
        else:
            dmt_array.append({'DMTdate':ddates[i], 'DMTvalues':values[i]})

    context = {
        "MAIN_ARRAY": main_array,
        "DMT_ARRAY":dmt_array,
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

    # if request.method == "GET":
    # ticker = request.GET.get('ticker')
    # startDate = request.GET.get('startDate')
    # endDate = request.GET.get('endDate')
    # graphValue = request.GET.get('graphValue')

    formula_data, r_squared, ticker_date, ticker_target, p = ExponRegressPrediction(ticker, graphValue, startDate, endDate)

    context = {
        'formula_data':formula_data,
        'r_squared':r_squared,
        "formula":str(p),
        'ticker_date':ticker_date,
        'ticker_target':ticker_target,
    }

    return Response(context)

@api_view(['GET', 'POST'])
def LogPrediction(request):
    Serializer_class = BasePredSerializer
    serializer = Serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    ticker = serializer.data.get('ticker')
    startDate = serializer.data.get('startDate')
    endDate = serializer.data.get('endDate')
    graphValue = serializer.data.get('graphValue')

    # if request.method == "GET":

    #     ticker = request.GET.get('ticker')
    #     startDate = request.GET.get('startDate')
    #     endDate = request.GET.get('endDate')
    #     graphValue = request.GET.get('graphValue')

    formula_data, r_squared, ticker_date, ticker_target, p = LogPredictions(ticker, graphValue, startDate, endDate)

    context = {
        'formula_data':formula_data,
        'r_squared':r_squared,
        "formula":str(p),
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

    # if request.method == "GET":

    #     ticker = request.GET.get('ticker')
    #     startDate = request.GET.get('startDate')
    #     endDate = request.GET.get('endDate')
    #     graphValue = request.GET.get('graphValue')
    #     power = request.GET.get('power')

    formula_data, r_squared, ticker_date, ticker_target, p = polyPredictions(ticker, graphValue, startDate, endDate, power)

    context = {
        'formula_data':formula_data,
        'r_squared':r_squared,
        "formula":str(p),
        'ticker_date':ticker_date,
        'ticker_target':ticker_target,
    }

    return Response(context)