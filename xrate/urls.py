from django.urls import path, include
from rest_framework import routers

from .views import XRateViewSet

router = routers.DefaultRouter()
router.register(r'xrate', XRateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
