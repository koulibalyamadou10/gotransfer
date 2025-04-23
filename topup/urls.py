from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TopupViewSet

router = DefaultRouter()
router.register(r'topup', TopupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
