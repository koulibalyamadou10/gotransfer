from rest_framework import serializers
from account.models import CustomUser
from beneficiary.serializers import BeneficiarySerializer

class CustomUserCreateSerializer(serializers.ModelSerializer):
    beneficiaries = BeneficiarySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('first_name', 'last_name', 'email', 'phone_number', 
                'address', 'role', 'email_verified_at', 'email_verified',
                'id_card', 'id_card_exp_date', 'bio', 'image', 'user_uuid', 'beneficiaries',
                'password', 'balance', 'currency', 'commission', 'sponsor_email', 'country')
        
    def validate_sponsor_email(self, value):
        if value:
            try:
                CustomUser.objects.get(email=value)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Aucun utilisateur trouvé avec cet email de parrainage.")
        return value

class CustomUserSerializer(serializers.ModelSerializer):
    beneficiaries = BeneficiarySerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = '__all__'
