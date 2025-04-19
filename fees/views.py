from drf_yasg import openapi
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from fees import models
from fees.models import Fees
from fees.serializers import FeesSerializer
from decimal import Decimal


# Create your views here.
class FeesViewSet(viewsets.ModelViewSet):
    queryset = models.Fees.objects.all().order_by('-created_at')
    serializer_class = FeesSerializer

    """
    {
        'src_country': 'Canada',
        'dest_country': 'Guinea',
        'amount': 100,
    }
    """
    @swagger_auto_schema(
        operation_description="Permet d'obtenir les frais de transfert d'une transaction",
        methods=['POST'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['amount', 'src_country', 'dest_country'],
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                'src_country': openapi.Schema(type=openapi.TYPE_STRING),
                'dest_country': openapi.Schema(type=openapi.TYPE_STRING),
            },
            examples={
                'amount': 100,
                'src_country': 'Canada',
                'dest_country': 'Guinea',
            }
        )
    )
    @action(
        detail=False, 
        methods=['POST'], 
        url_name='obtain_fees', 
        permission_classes=[IsAuthenticated], 
        authentication_classes=[JWTAuthentication]
    )
    def obtain_fee(self, request):
        src_country = request.data.get('src_country')
        dest_country = request.data.get('dest_country')
        amount = request.data.get('amount')

        if not src_country or not dest_country or not amount:
            return Response(
                {'message': 'src_country, dest_country, et amount sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = Decimal(amount)
        except ValueError:
            return Response({'message': 'amount doit être un nombre'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fees = Fees.objects.filter(
                src_country=src_country,
                dst_country=dest_country,
                from_amount__lte=amount,
                to_amount__gte=amount
            ).first()

            if not fees:
                return Response({'message': 'Aucun tarif trouvé pour cette plage de montant'}, status=status.HTTP_404_NOT_FOUND)

            # Calcul total des frais
            fixed_fee = fees.fees
            percentage_fee = (amount * fees.percentage_fees) / 100
            total_fee = round(fixed_fee + percentage_fee, 2)

            return Response({
                'fixed_fee': fixed_fee,
                'percentage_fee': round(percentage_fee, 2),
                'total_fee': total_fee,
                'currency': request.user.currency,
                'from': fees.from_amount,
                'to': fees.to_amount,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)