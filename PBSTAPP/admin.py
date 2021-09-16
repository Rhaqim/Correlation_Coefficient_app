from PBSTAPP.models import *
from django.contrib import admin

# Register your models here.
admin.site.register(StockTickers)
admin.site.register(ForexTickers)
admin.site.register(CryptoTickers)
admin.site.register(IndexTickers)

admin.site.register(USStockTicker)
admin.site.register(USIndexTicker)