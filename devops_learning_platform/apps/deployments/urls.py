from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnvironmentViewSet, ServiceViewSet, DeploymentViewSet

router = DefaultRouter()
router.register('environments', EnvironmentViewSet, basename='environment')
router.register('services', ServiceViewSet, basename='service')
router.register('deployments', DeploymentViewSet, basename='deployment')

urlpatterns = [
    path('', include(router.urls)),
]
