from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class GeoPostSerializer(serializers.ModelSerializer):
    geo_protocol = serializers.CharField(source='protocol', max_length=200)
