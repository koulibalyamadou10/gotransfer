from rest_framework import serializers
from .models import Topup

class TopupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topup
        fields = '__all__'