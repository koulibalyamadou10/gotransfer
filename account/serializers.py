from rest_framework import serializers
from account.models import CustomUser
from beneficiary.serializers import BeneficiarySerializer
from django.utils import timezone
from remittance.serializers import RemittanceSerializer

class CustomUserCreateSerializer(serializers.ModelSerializer):
    beneficiaries = BeneficiarySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}
        fields = ( 'id', 'first_name', 'last_name', 'email', 'phone_number', 
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
    remittances_today = serializers.SerializerMethodField()
    remittances_last = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 
                'address', 'role', 'email_verified_at', 'email_verified',
                'id_card', 'id_card_exp_date', 'bio', 'image', 'user_uuid', 'beneficiaries',
                'password', 'balance', 'currency', 'commission', 'sponsor_email', 
                'country', 'remittances_today', 'remittances_last']
    def get_remittances_last(self, obj):
        # Assuming you have a Remittance model with a foreign key to CustomUser
        from remittance.models import Remittance
        return RemittanceSerializer(
            Remittance.objects.filter(sender=obj).order_by('-created_at')[:5],
            many=True, 
            context=self.context
        ).data

    def get_remittances_today(self, obj):
        # Assuming you have a Remittance model with a foreign key to CustomUser
        from remittance.models import Remittance
        today = timezone.now().date()
        return RemittanceSerializer(
            Remittance.objects.filter(sender=obj, created_at__date=today),
            many=True, 
            context=self.context
        ).data
