from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    #HOMEPAGE
    path('', views.Homepage, name='homepage'),

    # #INDICES
    # path('indices/', views.indexhomepage, name='indices' ),
    # path('indices/indexhloc/', views.getIndexHLOC, name='indexhloc' ),

    # #FOREX
    path('forex/', views.forexhomepage, name='forex'),
    # path('forex/forexhloc/', views.getforexHLOC, name='forexhloc' ),

    # #CRYPTO
    # path('crypto/', views.Cryptohomepage, name='crypto'),
    # path('crypto/cryptohloc/', views.getCryptoHLOC, name='cryptohloc' ),

    #TESTS
    path('v2/forex', views.forexV2, name='forex_v2'),
    path('v2/crypto', views.cryptoV2, name='crypto_v2'),
    path('v2/index', views.indexV2, name='index_v2'),
    path('v2/stock', views.stockV2, name='stock_v2'),
]