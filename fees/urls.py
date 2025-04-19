from django.urls import path, include
from rest_framework import routers

from .views import FeesViewSet

router = routers.DefaultRouter()
router.register(r'fees', FeesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
