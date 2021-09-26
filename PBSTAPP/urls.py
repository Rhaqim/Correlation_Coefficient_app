from django.urls import path
from . import views

urlpatterns = [
    #HOMEPAGE
    path('', views.Homepage, name='homepage'),

    # #FOREX
    path('forex/', views.forexhomepage, name='forex'),

    #APIs
    path('v2/forex', views.forexV2, name='forex_v2'),
    path('v2/crypto', views.cryptoV2, name='crypto_v2'),
    path('v2/index', views.indexV2, name='index_v2'),
    path('v2/stock', views.stockV2, name='stock_v2'),

    path('v2/stock_country', views.Stock_country),
    path('v2/index_country', views.Index_country),

    path('v2/DMT', views.DailyMatchTrend),
    path('v2/correlation', views.Correlation),
]