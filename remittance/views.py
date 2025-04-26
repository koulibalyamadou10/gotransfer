from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .serializers import RemittanceCreateSerializer
from .models import Remittance

# Utility function to generate a transaction ID
def generate_transaction_id():
    import uuid
    return str(uuid.uuid4())


# Create your views here.
class RemittanceViewSet(viewsets.ModelViewSet):
    """
    API permettant de gérer les transactions.

    🛠 **Endpoints disponibles** :

    | Méthode | URL                       | Action                  |
    |---------|---------------------------|-------------------------|
    | GET     | `/remittance`                | Lister                  |
    | POST    | `/remittance`                | Ajouter                 |
    | GET     | `/remittance/{remittance_uuid}`    | Voir                    |
    | PUT     | `/remittance/{remittance_uuid}`    | Modifier                |
    | PATCH   | `/remittance/{remittance_uuid}`    | Modifier partiellement  |
    | DELETE  | `/remittance/{remittance_uuid}`    | Supprimer               |
    """

    serializer_class = RemittanceCreateSerializer
    queryset = Remittance.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'remittance_uuid'
    lookup_url_kwarg = 'remittance_uuid'

    def create(self, request, *args, **kwargs):
        """
        Créer une nouvelle transaction.
        """
        request.data['customer'] = request.user.id
        request.data['transaction_id'] = generate_transaction_id()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, 201)
