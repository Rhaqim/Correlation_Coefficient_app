from PBSTAPP.models import *
from django.contrib import admin

# Register your models here.
admin.site.register(StockTickers)
admin.site.register(ForexTickers)
admin.site.register(CryptoTickers)
admin.site.register(IndexTickers)

admin.site.register(USStockTicker)
admin.site.register(USIndexTicker)

# # Register your models here.
# admin.site.register(cryptoexchanges)
# admin.site.register(cryptocurrency_base)
# admin.site.register(cryptocurrency_quote)
# admin.site.register(cryptolist)

# # Register your models here.
# admin.site.register(forexcurrency_base)
# admin.site.register(forexcurrency_quote)
# admin.site.register(Forexlist)

# # Register your models here.
# admin.site.register(IndexList)
# admin.site.register(indexcountries)
# admin.site.register(indexcurrency)