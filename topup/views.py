from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import TopupCreateSerializer
from .models import Topup
from utils.utils import generate_transaction_id
from rest_framework.response import Response
import requests
from gotransfer import settings

# Create your views here.
class TopupViewSet(viewsets.ModelViewSet):
    """
    API permettant de gérer les recharges.

    🛠 **Endpoints disponibles** :

    | Méthode | URL                       | Action                  |
    |---------|---------------------------|-------------------------|
    | GET     | `/topup_uuid`                | Lister                  |
    | POST    | `/topup_uuid`                | Ajouter                 |
    | GET     | `/topup_uuid/{topup_uuid}`    | Voir                    |
    | PUT     | `/topup_uuid/{topup_uuid}`    | Modifier                |
    | PATCH   | `/topup_uuid/{topup_uuid}`    | Modifier partiellement  |
    | DELETE  | `/topup_uuid/{topup_uuid}`    | Supprimer               |
    """

    serializer_class = TopupCreateSerializer
    queryset = Topup.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'topup_uuid'
    lookup_url_kwarg = 'topup_uuid'

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['transaction_id'] = generate_transaction_id()
        data['user'] = request.user.id

        if request.user.balance < data['price']:
            return Response({"detail": "Solde insuffisant"}, status=400)

        # Verifier si le numero de telephone du user connecte commence par + si non remettre le +
        phone_number = data.get('phone_number')
        if not phone_number:
            return Response({"detail": "Le numéro de téléphone est requis"}, status=400)
        
        product_id = data.get('product_id')
        if not product_id:
            return Response({"detail": "Le product_id est requis"}, status=400)
        
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number

        # faire la transactions avec l'api externe
        data_to_transaction = {
            "external_id": data['transaction_id'],
            "product_id": product_id,
            "auto_confirm": True,
            "credit_party_identifier": {
                "mobile_number": phone_number,
            }
        }
        response = requests.post(
            settings.SANDBOX_URL_TRANSACTION_ASYNC,
            json=data_to_transaction,
            auth=(settings.SANDBOX_API_KEY, settings.SANDBOX_API_SECRET), 
        )

        if response.status_code != 200:
            return Response({"detail": "Erreur lors de la requête à l'API externe"}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        request.user.balance -= data['price']
        request.user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Endpoint pour lister les produits disponibles pour un operateur
    @action(
        detail=False, 
        methods=['post'],
        url_path='products',
        url_name='products',
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def list_products(self, request, *args, **kwargs):
        print(request.data)
        # Verifier si le numero de telephone du user connecte commence par + si non remettre le +
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"detail": "Le numéro de téléphone est requis"}, status=400)
        
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number

        # Envoyer une requete a l'API externe pour recuperer l'operateur
        response = requests.post(
            settings.SANDBOX_URL_LOOKUP_NUMBER,
            json={'mobile_number': phone_number},
            auth=(settings.SANDBOX_API_KEY, settings.SANDBOX_API_SECRET), 
        )

        print(response.status_code)
        print(response.json())

        if response.status_code != 200:
            return Response({"detail": "Erreur lors de la requête à l'API externe"}, status=400)
        operator_id = response.json()[0]['id']

        # lister les produits disponibles pour ce operateur
        response = requests.get(
            f"{settings.SANDBOX_URL_LOOKUP_LIST_PRODUCT}?operator_id={operator_id}&service_id=1",
            auth=(settings.SANDBOX_API_KEY, settings.SANDBOX_API_SECRET), 
        )
        operator_products = response.json()
        print(operator_products)

        return Response(operator_products, status=200)
