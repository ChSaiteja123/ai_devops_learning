from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArchitectureDiagramViewSet

router = DefaultRouter()
router.register('', ArchitectureDiagramViewSet, basename='architecture')

urlpatterns = [
    path('', include(router.urls)),
]
