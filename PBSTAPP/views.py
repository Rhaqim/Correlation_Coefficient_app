from PBSTAPP.serializers import SearchSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ForexTickers, CryptoTickers, USIndexTicker, USStockTicker
from decouple import config
from requests_cache.session import CachedSession
from .functions import percentagechange, stockAnalysis, get_client_ip, get_geolocation_for_ip, get_corresponding_currency
import json

requests = CachedSession()
token12 = config('TWELVEDATATOKEN')
tokeniex = config('IEXTOKEN')

@api_view(['GET'])
def Homepage(request):
    stuff = "Hello World"

    context = {
        'stuff':stuff
    }

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
    against = against

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

    if against == 'stock':
        comp = USStockTicker.objects.all()[:20]
    elif against == 'crypto':
        comp = CryptoTickers.objects.all()[:20]
    elif against == 'index':
        comp = USIndexTicker.objects.all()[:20]
    elif against == 'forex':
        comp = ForexTickers.objects.all()[:20]

    # comp = CryptoTickers.objects.all()[:120]
    col = []
    thelist = []
    for item in comp:
        thelist.append(item.symbol)

    for stuff in thelist:
        try:
            stv2 = stockAnalysis(Base_Symbol=symbolValue, Compare_Symbol=stuff, startdate=startDate, enddate=endDate, hloc=hloc)
            col.append({stuff:stv2})
        except:
            pass

    context = {
        'DMT': datatrend['values'],
        'coefficient': col,
        'pctchange': res
    }

    return context


@api_view(['GET'])
def forexV2(request):

    context = generalPurpose(request, 'forex')

    return Response(context)

@api_view(['GET'])
def cryptoV2(request):

    context = generalPurpose(request, 'crypto')

    return Response(context)

@api_view(['GET'])
def indexV2(request):

    context = generalPurpose(request, 'index')

    return Response(context)

@api_view(['GET'])
def stockV2(request):

    context = generalPurpose(request, 'stock')

    return Response(context)


# #Homepage
# @api_view(['GET'])
# def Cryptohomepage(request):
#     dropdown = CryptoTickers.objects.all()

#     serializer = CryptoSerializer(dropdown, many=True)

#     context = serializer.data

#     return Response(context)


# #Ajax
# def getCryptoHLOC(request):

#     if request.method == 'GET' and request.is_ajax():

#         symbolValue = request.GET.get('indexSymbolValue')
#         startDate = request.GET.get('startdate_aa')
#         endDate = request.GET.get('enddate_aa')
#         hloc = request.GET.get('ohlc_a')
#         against = request.GET.get('against')

#         datatrend, pctchange = percentagechange(symbol=symbolValue, startdate=startDate, enddate=endDate, hloc=hloc)

#         pctchange.pop(0)

#         checking = datatrend['values']

#         datetimelist = []

#         for i in checking:
#             datetimelist.append(i['datetime'])
        
#         rateofchange = []

#         for k in pctchange:
#             rateofchange.append(k * -100)

#         res = {}

#         for key in datetimelist:
#             for value in rateofchange:
#                 res[key] = value
#                 rateofchange.remove(value)
#                 break 

#         if against == 'stock':
#             comp = USStockTicker.objects.all()[:20]
#         elif against == 'crypto':
#             comp = cryptolist.objects.all()[:20]
#         elif against == 'index':
#             comp = USIndexTicker.objects.all()[:20]
#         elif against == 'forex':
#             comp = ForexTickers.objects.all()[:20]

#         # comp = CryptoTickers.objects.all()[:120]
#         col = []
#         thelist = []
#         for item in comp:
#             thelist.append(item.symbol)

#         for stuff in thelist:
#             try:
#                 stv2 = stockAnalysis(Base_Symbol=symbolValue, Compare_Symbol=stuff, startdate=startDate, enddate=endDate, hloc=hloc)
#                 col.append({stuff:stv2})
#             except:
#                 pass

#     context = {
#         'DMT': datatrend['values'],
#         'coefficient': col,
#         'pctchange': res
#     }

#     return JsonResponse(context)

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

# #Ajax
# def getforexHLOC(request):

#     if request.method == 'GET' and request.is_ajax():

#         symbolValue = request.GET.get('forexSymbolValue')
#         startDate = request.GET.get('startdate_aa')
#         endDate = request.GET.get('enddate_aa')
#         hloc = request.GET.get('ohlc_a')
#         against = request.GET.get('against')

#         # datatrend = dailymatchtrend(symbol=symbolValue)

#         datatrend, pctchange = percentagechange(symbol=symbolValue, startdate=startDate, enddate=endDate, hloc=hloc)

#         pctchange.pop(0)

#         checking = datatrend['values']

#         datetimelist = []

#         for i in checking:
#             datetimelist.append(i['datetime'])
        
#         rateofchange = []

#         for k in pctchange:
#             rateofchange.append(k * -100)

#         res = {}

#         for key in datetimelist:
#             for value in rateofchange:
#                 res[key] = value
#                 rateofchange.remove(value)
#                 break 

#         if against == 'stock':
#             comp = USStockTicker.objects.all()[:20]
#         elif against == 'crypto':
#             comp = cryptolist.objects.all()[:20]
#         elif against == 'index':
#             comp = USIndexTicker.objects.all()[:20]
#         elif against == 'forex':
#             comp = Forexlist.objects.all()[:20]

#         # comp = CryptoTickers.objects.all()[:120]
#         col = []
#         thelist = []
#         for item in comp:
#             thelist.append(item.symbol)

#         for stuff in thelist:
#             try:
#                 stv2 = stockAnalysis(Base_Symbol=symbolValue, Compare_Symbol=stuff, startdate=startDate, enddate=endDate, hloc=hloc)
#                 col.append({stuff:stv2})
#             except:
#                 pass

#     context = {
#         'DMT': datatrend['values'],
#         'coefficient': col,
#         'pctchange': res,
#     }

#     return JsonResponse(context)

# # Create your views here.
# def indexhomepage(request):
#     dropdown = USIndexTicker.objects.all()

#     context = {
#         'indexdropdown':dropdown,
#     }
#     return render(request, "indices.html", context)


# #Ajax
# def getIndexHLOC(request):

#     if request.method == 'GET' and request.is_ajax():

#         symbolValue = request.GET.get('indexSymbolValue')
#         startDate = request.GET.get('startdate_aa')
#         endDate = request.GET.get('enddate_aa')
#         hloc = request.GET.get('ohlc_a')
#         against = request.GET.get('against')

#         # datatrend = dailymatchtrend(symbol=symbolValue)

#         datatrend, pctchange = percentagechange(symbol=symbolValue, startdate=startDate, enddate=endDate, hloc=hloc)

#         pctchange.pop(0)

#         checking = datatrend['values']

#         datetimelist = []

#         for i in checking:
#             datetimelist.append(i['datetime'])
        
#         rateofchange = []

#         for k in pctchange:
#             rateofchange.append(k * -100)

#         res = {}

#         for key in datetimelist:
#             for value in rateofchange:
#                 res[key] = value
#                 rateofchange.remove(value)
#                 break 

#         if against == 'stock':
#             comp = USStockTicker.objects.all()[:20]
#         elif against == 'crypto':
#             comp = cryptolist.objects.all()[:20]
#         elif against == 'index':
#             comp = USIndexTicker.objects.all()[:20]
#         elif against == 'forex':
#             comp = ForexTickers.objects.all()[:20]

#         # comp = CryptoTickers.objects.all()[:120]
#         col = []
#         thelist = []
#         for item in comp:
#             thelist.append(item.symbol)

#         for stuff in thelist:
#             try:
#                 stv2 = stockAnalysis(Base_Symbol=symbolValue, Compare_Symbol=stuff, startdate=startDate, enddate=endDate, hloc=hloc)
#                 col.append({stuff:stv2})
#             except:
#                 pass

#     context = {
#         'DMT': datatrend['values'],
#         'coefficient': col,
#         'pctchange': res
#     }

#     return JsonResponse(context)

