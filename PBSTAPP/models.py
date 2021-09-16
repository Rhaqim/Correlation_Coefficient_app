from django.db import models

# Create your models here.

class cryptoexchanges(models.Model):
    exchanges = models.CharField(max_length=150)

    def clean(self):
        self.exchanges = self.exchanges.upper()

    def __str__(self):
        return '{}'.format(self.exchanges)



class cryptocurrency_base(models.Model):
    currency_base = models.CharField(max_length=50)

    def clean(self):
        self.currency_base = self.currency_base.upper()

    def __str__(self):
        return '{}'.format(self.currency_base)



class cryptocurrency_quote(models.Model):
    currency_quote = models.CharField(max_length=50)

    def clean(self):
        self.currency_quote = self.currency_quote.upper()

    def __str__(self):
        return '{}'.format(self.currency_quote)


class cryptolist(models.Model):
    symbol = models.CharField(max_length=50)
    available_exchanges = models.ManyToManyField(to=cryptoexchanges, blank=True)
    currency_base = models.ManyToManyField(to=cryptocurrency_base, blank=True)
    currency_quote = models.ManyToManyField(to=cryptocurrency_quote, blank=True)

    def clean(self):
        self.symbol = self.symbol.upper()

    def __str__(self):
        return '{}'.format(self.symbol)


#COUNTRIES
class indexcountries(models.Model):
    country = models.CharField(max_length=150)

    def clean(self):
        self.country = self.country.upper()

    def __str__(self):
        return '{}'.format(self.country)

#CURRENCIES
class indexcurrency(models.Model):
    currency = models.CharField(max_length=150)

    def clean(self):
        self.currency = self.currency.upper()

    def __str__(self):
        return '{}'.format(self.currency)

class IndexList(models.Model):
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    country = models.ManyToManyField(to=indexcountries)
    currency = models.ManyToManyField(to=indexcurrency)

    def clean(self):
        self.name = self.name.upper()
        self.symbol = self.symbol.upper()

    def __str__(self):
        return '{} - {}'.format(self.name, self.symbol)



class forexcurrency_base(models.Model):
    currency_base = models.CharField(max_length=50)

    def clean(self):
        self.currency_base = self.currency_base.upper()

    def __str__(self):
        return '{}'.format(self.currency_base)



class forexcurrency_quote(models.Model):
    currency_quote = models.CharField(max_length=50)

    def clean(self):
        self.currency_quote = self.currency_quote.upper()

    def __str__(self):
        return '{}'.format(self.currency_quote)




class Forexlist(models.Model):
    symbol = models.CharField(max_length=20)
    currency_group = models.CharField(max_length=100)
    currency_base = models.ManyToManyField(to=forexcurrency_base)
    currency_quote = models.ManyToManyField(to=forexcurrency_quote)

    def clean(self):
        self.symbol = self.symbol.upper()

    def __str__(self):
        return self.symbol


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
