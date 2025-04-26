from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Beneficiary  
from .serializers import BeneficiaryCreateSerializer  
from .serializers import BeneficiarySerializer  

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
    
    @action(
        detail=False,
        methods=['post'],
        url_path='get_country_code',
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )   
    def get_country_code(self, request, *args, **kwargs):
        """
        Récupérer le code du pays à partir du numéro de téléphone.
        """
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Le numéro de téléphone est requis."}, status=status.HTTP_400_BAD_REQUEST)

        beneficiary = self.get_queryset().filter(phone_number=phone_number).first()
        if not Beneficiary:
            return Response(
                {"detail": "Aucun bénéficiaire trouvé avec ce numéro de téléphone."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(BeneficiarySerializer(beneficiary, context={'request': request}).data, status=status.HTTP_200_OK)