# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .serializers import DestinationCreateSerializer
from .models import Destination

# Create your views here.
class DestinationViewSet(viewsets.ModelViewSet):
    """
    API permettant de gérer les destinations.

    🛠 **Endpoints disponibles** :

    | Méthode | URL                       | Action                  |
    |---------|---------------------------|-------------------------|
    | GET     | `/destination`                | Lister                  |
    | POST    | `/destination`                | Ajouter                 |
    | GET     | `/destination/{destination_uuid}`    | Voir                    |
    | PUT     | `/destination/{destination_uuid}`    | Modifier                |
    | PATCH   | `/destination/{destination_uuid}`    | Modifier partiellement  |
    | DELETE  | `/destination/{destination_uuid}`    | Supprimer               |
    """

    serializer_class = DestinationCreateSerializer
    queryset = Destination.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'destination_uuid'
    lookup_url_kwarg = 'destination_uuid'

    @action(
        detail=False,
        methods=['get'],
        url_path='get_destinations',
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def get_destinations(self, request):
        """
        Récupérer toutes les destinations.
        """
        destinations = Destination.objects.all()
        serializer = self.get_serializer(destinations, many=True)
        return Response(serializer.data, status=200)
