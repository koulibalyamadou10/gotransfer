from django.urls import path
from rest_framework import routers

from .views import FeesViewSet

router = routers.DefaultRouter()
router.register(r'', FeesViewSet)

urlpatterns = [
    path('fees/', router.urls, name='fees'),
]