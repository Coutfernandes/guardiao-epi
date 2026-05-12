from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CameraViewSet, ConfiguracaoEPIViewSet

router = DefaultRouter()
router.register(r'cameras', CameraViewSet)
router.register(r'configuracoes-epi', ConfiguracaoEPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
]