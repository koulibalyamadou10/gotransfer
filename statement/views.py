from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import StatementCreateSerializer
from .models import Statement

# Create your views here.
class StatementViewSet(viewsets.ModelViewSet):

    serializer_class = StatementCreateSerializer
    queryset = Statement.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'statement_uuid'
    lookup_url_kwarg = 'statement_uuid'

     