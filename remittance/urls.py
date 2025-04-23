from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RemittanceViewSet

router = DefaultRouter()
router.register(r'remittance', RemittanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
