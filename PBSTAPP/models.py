from django.db import models

class USStockTicker(models.Model):
    symbol = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)
    exchange = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.name)

class USIndexTicker(models.Model):
    symbol = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.name)

class StockTickers(models.Model):
    symbol = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)
    exchange = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    type = models.CharField(max_length=200)
    
    

    def clean(self):
        self.symbol = self.symbol.upper()

    def __str__(self):
        return '{} - {} - {}'.format(self.symbol, self.name, self.exchange)


class ForexTickers(models.Model):
    symbol = models.CharField(max_length=200)
    currency_group = models.CharField(max_length=200)
    currency_base = models.CharField(max_length=200)
    currency_quote = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)
    
    

    def clean(self):
        self.symbol = self.symbol.upper()

    def __str__(self):
        return '{}'.format(self.symbol)


class IndexTickers(models.Model):
    symbol = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)
    
    

    def clean(self):
        self.symbol = self.symbol.upper()

    def __str__(self):
        return '{} - {}'.format(self.symbol, self.name)


class CryptoTickers(models.Model):
    symbol = models.CharField(max_length=200)
    available_exchanges = models.CharField(max_length=200)
    currency_base = models.CharField(max_length=200)
    currency_quote = models.CharField(max_length=200)
    
    

    def clean(self):
        self.symbol = self.symbol.upper()

    def __str__(self):
        return '{}'.format(self.symbol)
