from rest_framework import serializers

from fees.models import Fees

class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = '__all__'