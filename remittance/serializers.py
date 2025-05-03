from rest_framework import serializers
from .models import Remittance

class RemittanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remittance
        fields = '__all__'

class RemittanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remittance
        fields = '__all__'