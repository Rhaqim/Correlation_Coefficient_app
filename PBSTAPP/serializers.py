from rest_framework import serializers
from .models import *

class SearchSerializer(serializers.Serializer):
    symbolValue = serializers.CharField()
    startdate = serializers.DateField()
    enddate = serializers.DateField()
    hloc = serializers.CharField()
