from rest_framework import serializers
from .models import *

class SearchSerializer(serializers.Serializer):
    symbolValue = serializers.CharField()
    startdate = serializers.DateField()
    enddate = serializers.DateField()
    hloc = serializers.CharField()

class CountrySerializer(serializers.Serializer):
    country = serializers.CharField()

class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexTickers
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTickers
        fields = '__all__'

class CountryExchangeSerializer(serializers.Serializer):
    country = serializers.CharField(required=False)
    exchange = serializers.CharField(required=False)

#Daily match trend
class DailyMatchtrendSerializer(serializers.Serializer):
    GRAPHVALUE_CHOICES = (
        ("high","High"),
        ("low", "Low"),
        ("open", "Open"),
        ("close", "Close")
    )
    numberOfDays = serializers.IntegerField()
    graphValue = serializers.ChoiceField(choices=GRAPHVALUE_CHOICES)
    percentageChange = serializers.IntegerField()