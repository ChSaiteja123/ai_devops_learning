from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidentViewSet, analyze

router = DefaultRouter()
router.register('incidents', IncidentViewSet, basename='incident')

urlpatterns = [
    path('', include(router.urls)),
    path('analyze/', analyze, name='aiops-analyze'),
]
