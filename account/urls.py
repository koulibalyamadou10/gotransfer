from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.views import CustomUserCreateViewSet

router = DefaultRouter()
router.register(r'account', CustomUserCreateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
