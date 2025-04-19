from rest_framework import serializers
from account.models import CustomUser

class CustomUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('first_name', 'last_name', 'email', 'phone_number', 
                'address', 'role', 'email_verified_at', 'email_verified',
                'card', 'card_exp_date', 'bio', 'image', 'user_uuid',
                'password', 'balance', 'currency', 'commission', 'sponsor_email')

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = '__all__'
