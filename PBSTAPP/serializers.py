from rest_framework import serializers
from .models import *

class SearchSerializer(serializers.Serializer):
    symbolValue = serializers.CharField()
    startdate = serializers.DateField()
    enddate = serializers.DateField()
    hloc = serializers.CharField()

class ForexSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForexTickers
        fields = '__all__'

class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoTickers
        fields = '__all__'

class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexTickers
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTickers
        fields = '__all__'