from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OcorrenciaViewSet

router = DefaultRouter()
router.register(r'deteccao/ocorrencias', OcorrenciaViewSet, basename='ocorrencia')

urlpatterns = [
    path('', include(router.urls)),
    path('deteccao/processar/', OcorrenciaViewSet.as_view({'post': 'processar'})),
]