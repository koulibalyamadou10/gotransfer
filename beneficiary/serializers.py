from rest_framework import serializers
from .models import Beneficiary

class BeneficiaryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        read_only_fields = ('id', 'created_at', 'updated_at')               
        model = Beneficiary
        fields = ('id', 'customer', 'first_name', 'last_name', 'pays', 'country_code', 'country_currency', 'phone_number')

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ('id', 'first_name', 'last_name', 'pays', 'phone_number', 'country_code', 'country_currency', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')