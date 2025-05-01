from drf_yasg import openapi
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from xrate import models
from .models import XRate
from .serializers import XRateCreateSerializer
from decimal import Decimal
from fees.models import Fees
from beneficiary.models import Beneficiary

# Create your views here.
class XRateViewSet(viewsets.ModelViewSet):
    queryset = models.XRate.objects.all().order_by('-created_at')
    serializer_class = XRateCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=['post'],
        url_path='convert',
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )   
    def convert(self, request, *args, **kwargs):
        """
        Récupérer le code du pays à partir du numéro de téléphone.
        Exemple de requête : 
        {
            "phone_number": "+224123456789",
            "src_currency": "CAD",
            "src_country": "Canada",
            "dst_currency": "GNF",
            "dst_country": "Guinea",
            "amount": 100
        }
        """
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Le numéro de téléphone est requis."}, status=status.HTTP_400_BAD_REQUEST)

        src_currency = request.data.get('src_currency')
        dst_currency = request.data.get('dst_currency')
        src_country = request.data.get('src_country')
        dst_country = request.data.get('dst_country')
        amount = request.data.get('amount')

        print(f'{phone_number} {src_currency} {dst_currency} {src_country} {dst_country} {amount}')

        # if not src_currency or not dst_currency or not amount or not src_country or not dst_country:
        #     return Response(
        #         {'detail': 'src_currency, dst_currency, src_country, dst_country et amount sont requis'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        
        try:
            amount = Decimal(amount)
        except ValueError:
            return Response({'detail': 'amount doit être un nombre'}, status=status.HTTP_400_BAD_REQUEST)

        beneficiary = Beneficiary.objects.get(phone_number=phone_number)
        if not beneficiary:
            return Response(
                {"detail": "Aucun bénéficiaire trouvé avec ce numéro de téléphone."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            fees = Fees.objects.filter(
                src_country=src_country,
                dst_country=dst_country,
                from_amount__lte=amount,
                to_amount__gte=amount
            ).first()

            if not fees:
                return Response({'detail': 'Aucun tarif trouvé pour cette plage de montant'}, status=status.HTTP_404_NOT_FOUND)
            
            xrates = XRate.objects.filter(
                src_currency=src_currency,
                dst_currency=dst_currency
            ).first()
            if not xrates:
                return Response({'detail': 'Aucun taux de change trouvé pour cette plage de montant'}, status=status.HTTP_404_NOT_FOUND)
            
            # Calcul total des frais
            fixed_fee = fees.fees
            percentage_fee = (amount * fees.percentage_fees) / 100
            total_fee = round(fixed_fee + percentage_fee, 2)

            return Response({
                'fixed_fee': fixed_fee,
                'percentage_fee': round(percentage_fee, 2),
                'total_fee': total_fee,
                'total_amount': round(amount + total_fee, 2),
                'currency': request.user.currency,
                'from': fees.from_amount,
                'to': fees.to_amount,
                'ratio': xrates.ratio,
                "country_code": beneficiary.country_code
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)