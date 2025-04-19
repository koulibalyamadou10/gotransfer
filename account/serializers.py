from rest_framework import serializers
from account.models import CustomUser

class CustomUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'password')

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = '__all__'
