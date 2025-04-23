from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import RemittanceCreateSerializer
from .models import Remittance


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
