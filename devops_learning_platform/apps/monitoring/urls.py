from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MetricSnapshotViewSet, AlertRuleViewSet,
    AlertViewSet, HealthCheckViewSet, monitoring_dashboard,
)

router = DefaultRouter()
router.register('metrics', MetricSnapshotViewSet, basename='metric-snapshot')
router.register('alert-rules', AlertRuleViewSet, basename='alert-rule')
router.register('alerts', AlertViewSet, basename='alert')
router.register('health', HealthCheckViewSet, basename='health-check')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', monitoring_dashboard, name='monitoring-dashboard'),
]
