from rest_framework import serializers

from .models import XRate

class XRateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = XRate
        fields = '__all__'

class XRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = XRate
        fields = '__all__'