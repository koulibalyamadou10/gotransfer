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
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        request.user.balance -= data['price']
        request.user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
