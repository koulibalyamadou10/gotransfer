from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.models import CustomUser
from account.serializers import CustomUserCreateSerializer, CustomUserSerializer


# Create your views here.
class CustomUserCreateViewSet(viewsets.ModelViewSet):
    """
    API permettant de gérer les utilisateurs.

    🛠 **Endpoints disponibles** :

    | Méthode | URL                       | Action                  |
    |---------|---------------------------|-------------------------|
    | GET     | `/account`                | Lister                  |
    | POST    | `/account`                | Ajouter                 |
    | POST    | `/account/login`          | Se connecter            |
    | GET     | `/account/{user_uuid}`    | Voir                    |
    | PUT     | `/account/{user_uuid}`    | Modifier                |
    | PATCH   | `/account/{user_uuid}`    | Modifier partiellement  |
    | DELETE  | `/account/{user_uuid}`    | Supprimer               |
    """

    serializer_class = CustomUserCreateSerializer
    queryset = CustomUser.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'user_uuid'
    lookup_url_kwarg = 'user_uuid'

    @action(
        detail=False,
        methods=['post'],
        url_path='register',
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.set_sh()
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['post'],
        url_path='login',
        permission_classes=[AllowAny],
        authentication_classes=[],
    )    

    def login(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"detail": "Email and password sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Identifiant incorrect."}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"detail": "Identifiant incorrect."}, status=status.HTTP_404_NOT_FOUND)

        # Génération du token JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': CustomUserCreateSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    @action(
        detail=False, 
        methods=['delete'], 
        url_path='logout',
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def logout(self, request, *args, **kwargs):
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)

    @action(
        detail=False, 
        methods=['get'], 
        url_path='get_user',
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication], 
    )
    def get_user(self, request, *args, **kwargs):
        return Response(CustomUserSerializer(
            request.user,
            context={'request':request}
        ).data, status=status.HTTP_200_OK)