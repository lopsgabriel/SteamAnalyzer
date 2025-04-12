from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Steamlyzer.views import SteamAnalyzerViewSet

router = DefaultRouter()
router.register(r'steam', SteamAnalyzerViewSet, basename='steam-analyzer')

urlpatterns = [
    path('', include(router.urls)),
]
