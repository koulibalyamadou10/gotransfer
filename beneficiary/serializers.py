from rest_framework import serializers
from .models import Beneficiary

class BeneficiaryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Beneficiary
        fields = ('customer', 'first_name', 'last_name', 'pays', 'phone_number')

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ('id', 'first_name', 'last_name', 'pays', 'phone_number', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')