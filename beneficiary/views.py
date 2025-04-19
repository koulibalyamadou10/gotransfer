from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Beneficiary  
from .serializers import BeneficiaryCreateSerializer  

# Create your views here.
class BeneficiaryViewSet(viewsets.ModelViewSet):
    """
    API permettant de gérer les bénéficiaires.

    🛠 **Endpoints disponibles** :

    | Méthode | URL                       | Action                  |
    |---------|---------------------------|-------------------------|
    | GET     | `/beneficiary`            | Lister                  |
    | POST    | `/beneficiary`            | Ajouter                 |
    | GET     | `/beneficiary/{id}`       | Voir                    |
    | PUT     | `/beneficiary/{id}`       | Modifier                |
    | PATCH   | `/beneficiary/{id}`       | Modifier partiellement  |
    | DELETE  | `/beneficiary/{id}`       | Supprimer               |
    """

    serializer_class = BeneficiaryCreateSerializer  # Replace with your serializer class
    queryset = Beneficiary.objects.all().order_by('-id')  # Replace with your queryset
    permission_classes = [IsAuthenticated]  # Replace with your permission classes
    authentication_classes = [JWTAuthentication]  # Replace with your authentication classes
    lookup_field = 'beneficiary_uuid'  # Replace with your lookup field
    lookup_url_kwarg = 'beneficiary_uuid'  # Replace with your lookup URL kwarg

    @action(
        detail=False,
        methods=['post'],
        url_path='register',
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def register(self, request, *args, **kwargs):
        request.data['customer'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)