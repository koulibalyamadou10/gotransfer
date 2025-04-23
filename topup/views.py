from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import TopupCreateSerializer
from .models import Topup

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
    lookup_field = 'destination_uuid'
    lookup_url_kwarg = 'destination_uuid'
