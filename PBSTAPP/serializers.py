from rest_framework import serializers
from .models import *


#SEARCH SERIALIZERS
class SearchSerializer(serializers.Serializer):
    symbolValue = serializers.CharField()
    startdate = serializers.DateField()
    enddate = serializers.DateField()
    hloc = serializers.CharField()

class NameSearchSerializer(serializers.Serializer):
    name = serializers.CharField()

class CountrySerializer(serializers.Serializer):
    country = serializers.CharField()

class ExchangeSerializer(serializers.Serializer):
    exchange = serializers.CharField()

class CountryExchangeSerializer(serializers.Serializer):
    country = serializers.CharField(required=False)
    exchange = serializers.CharField(required=False)

#MODEL SERIALIZERS
class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexTickers
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTickers
        fields = '__all__'

#FEATURES SERIALIZERS

#HLOC CHOICES
GRAPHVALUE_CHOICES = (
        ("high","High"),
        ("low", "Low"),
        ("open", "Open"),
        ("close", "Close")
    )

#Daily match trend
class DailyMatchtrendSerializer(serializers.Serializer):
    DAYSCHOICE = (
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7")
    )

    CHANGE_CHOICE = (
        ("pctChange", "Percentage Change"),
        ("actChange", "Actual Value Change")
    )

    ticker = serializers.CharField()
    numberOfDays = serializers.ChoiceField(choices=DAYSCHOICE)
    graphValue = serializers.ChoiceField(choices=GRAPHVALUE_CHOICES)
    percentageChange = serializers.IntegerField()
    change_choice = serializers.ChoiceField(choices=CHANGE_CHOICE)

#Correlation Serializer
class CorrelationSerializer(serializers.Serializer):
    base_ticker = serializers.CharField()
    compare_tickers = serializers.ListField()
    startDate = serializers.DateField()
    endDate = serializers.DateField()
    graphValue = serializers.ChoiceField(choices=GRAPHVALUE_CHOICES)

#Prediction Serializer
class BasePredSerializer(serializers.Serializer):

    ticker = serializers.CharField()
    startDate = serializers.DateField()
    endDate = serializers.DateField()
    graphValue = serializers.ChoiceField(choices=GRAPHVALUE_CHOICES)

#Polynomial
class PowerPredSerializer(BasePredSerializer):

    POWER_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6")
    )

    power = serializers.ChoiceField(choices=POWER_CHOICES)