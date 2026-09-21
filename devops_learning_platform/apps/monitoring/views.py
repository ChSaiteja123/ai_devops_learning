"""
Monitoring Views.

ENDPOINTS:
----------
GET  /api/v1/monitoring/metrics/              → List metric snapshots
POST /api/v1/monitoring/metrics/              → Ingest a new metric snapshot
GET  /api/v1/monitoring/metrics/latest/       → Latest snapshot per service
GET  /api/v1/monitoring/alert-rules/          → List alert rules
POST /api/v1/monitoring/alert-rules/          → Create alert rule
GET  /api/v1/monitoring/alerts/               → List fired alerts
POST /api/v1/monitoring/alerts/{id}/resolve/  → Mark alert as resolved
GET  /api/v1/monitoring/health/               → List health check results
POST /api/v1/monitoring/health/               → Record a health check
GET  /api/v1/monitoring/dashboard/            → Aggregated monitoring dashboard
"""
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import MetricSnapshot, AlertRule, Alert, HealthCheck
from .serializers import (
    MetricSnapshotSerializer, AlertRuleSerializer,
    AlertSerializer, HealthCheckSerializer,
)


class MetricSnapshotViewSet(viewsets.ModelViewSet):
    """
    Ingest and query metric snapshots.
    Read: any authenticated user.
    Write: staff only (or ingestion service accounts).
    """
    queryset = MetricSnapshot.objects.all()
    serializer_class = MetricSnapshotSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service_name', 'source', 'namespace']
    ordering_fields = ['recorded_at']
    ordering = ['-recorded_at']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='latest')
    def latest(self, request):
        """Return the most recent snapshot for each unique service_name."""
        services = MetricSnapshot.objects.values_list('service_name', flat=True).distinct()
        result = []
        for svc in services:
            snap = MetricSnapshot.objects.filter(service_name=svc).order_by('-recorded_at').first()
            if snap:
                result.append(MetricSnapshotSerializer(snap).data)
        return Response(result)


class AlertRuleViewSet(viewsets.ModelViewSet):
    """CRUD for alert rules. Staff-only writes."""
    queryset = AlertRule.objects.select_related('created_by').all()
    serializer_class = AlertRuleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['severity', 'metric', 'is_active', 'service_name']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AlertViewSet(viewsets.ModelViewSet):
    """View and manage fired alerts."""
    queryset = Alert.objects.select_related('rule', 'acknowledged_by').all()
    serializer_class = AlertSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'severity', 'service_name']
    ordering = ['-fired_at']

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """POST /api/v1/monitoring/alerts/{id}/resolve/ — mark alert as resolved."""
        alert = self.get_object()
        if alert.status == 'resolved':
            return Response({'detail': 'Alert is already resolved.'}, status=status.HTTP_400_BAD_REQUEST)
        alert.status = 'resolved'
        alert.resolved_at = timezone.now()
        alert.acknowledged_by = request.user
        alert.save(update_fields=['status', 'resolved_at', 'acknowledged_by'])
        return Response(AlertSerializer(alert).data)

    @action(detail=True, methods=['post'])
    def silence(self, request, pk=None):
        """POST /api/v1/monitoring/alerts/{id}/silence/ — suppress a noisy alert."""
        alert = self.get_object()
        alert.status = 'silenced'
        alert.acknowledged_by = request.user
        alert.save(update_fields=['status', 'acknowledged_by'])
        return Response(AlertSerializer(alert).data)


class HealthCheckViewSet(viewsets.ModelViewSet):
    """Record and query service health checks."""
    queryset = HealthCheck.objects.all()
    serializer_class = HealthCheckSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service_name', 'status']
    ordering = ['-checked_at']

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def monitoring_dashboard(request):
    """
    GET /api/v1/monitoring/dashboard/
    Returns an aggregated view of platform health.
    """
    firing_alerts = Alert.objects.filter(status='firing')
    unhealthy = HealthCheck.objects.filter(status='unhealthy').values('service_name', 'endpoint', 'error_message', 'checked_at')

    # Latest snapshots per service
    services = MetricSnapshot.objects.values_list('service_name', flat=True).distinct()
    latest_metrics = []
    for svc in services:
        snap = MetricSnapshot.objects.filter(service_name=svc).order_by('-recorded_at').first()
        if snap:
            latest_metrics.append(MetricSnapshotSerializer(snap).data)

    return Response({
        'summary': {
            'total_services': len(services),
            'firing_alerts': firing_alerts.count(),
            'critical_alerts': firing_alerts.filter(severity='critical').count(),
            'unhealthy_services': HealthCheck.objects.filter(status='unhealthy').values('service_name').distinct().count(),
        },
        'firing_alerts': AlertSerializer(firing_alerts[:10], many=True).data,
        'unhealthy_services': list(unhealthy[:10]),
        'latest_metrics': latest_metrics,
    })
