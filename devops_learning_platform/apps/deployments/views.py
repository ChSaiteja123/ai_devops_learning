"""
Deployments Views.

ENDPOINTS:
----------
GET/POST /api/v1/deployments/environments/
GET/POST /api/v1/deployments/services/
GET/POST /api/v1/deployments/deployments/
POST     /api/v1/deployments/deployments/{id}/update-status/
POST     /api/v1/deployments/deployments/{id}/rollback/
POST     /api/v1/deployments/deployments/{id}/add-note/
GET      /api/v1/deployments/deployments/recent/
"""
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Environment, Service, Deployment, DeploymentNote
from .serializers import (
    EnvironmentSerializer, ServiceSerializer,
    DeploymentSerializer, DeploymentNoteSerializer,
    UpdateDeploymentStatusSerializer,
)


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related('owner').all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'tech_stack']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name', '')
        serializer.save(owner=self.request.user, slug=slugify(name))


class DeploymentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for deployments.
    Any authenticated user can view; only staff can trigger new ones.
    """
    queryset = Deployment.objects.select_related(
        'service', 'environment', 'triggered_by'
    ).prefetch_related('notes').all()
    serializer_class = DeploymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'service', 'environment']
    ordering = ['-triggered_at']

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(triggered_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        """POST /api/v1/deployments/deployments/{id}/update-status/ — CI/CD pipeline status webhook."""
        deployment = self.get_object()
        serializer = UpdateDeploymentStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        deployment.status = new_status

        if new_status == 'deploying' and not deployment.started_at:
            deployment.started_at = timezone.now()
        elif new_status in ('deployed', 'failed', 'rolled_back', 'cancelled'):
            deployment.completed_at = timezone.now()
            if 'error_log' in serializer.validated_data:
                deployment.error_log = serializer.validated_data['error_log']

        deployment.save()
        return Response(DeploymentSerializer(deployment).data)

    @action(detail=True, methods=['post'])
    def rollback(self, request, pk=None):
        """POST /api/v1/deployments/deployments/{id}/rollback/ — create a rollback deployment."""
        original = self.get_object()

        # Find the last successful deployment for the same service+environment (before this one)
        previous = Deployment.objects.filter(
            service=original.service,
            environment=original.environment,
            status='deployed',
            triggered_at__lt=original.triggered_at,
        ).order_by('-triggered_at').first()

        if not previous:
            return Response(
                {'detail': 'No previous successful deployment found to roll back to.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rollback_deployment = Deployment.objects.create(
            service=original.service,
            environment=original.environment,
            version=previous.version,
            git_commit=previous.git_commit,
            git_branch=previous.git_branch,
            docker_image=previous.docker_image,
            status='triggered',
            triggered_by=request.user,
            changelog=f'Rollback from v{original.version} to v{previous.version}',
            rolled_back_from=original,
        )

        # Mark original as rolled back
        original.status = 'rolled_back'
        original.completed_at = timezone.now()
        original.save(update_fields=['status', 'completed_at'])

        return Response(DeploymentSerializer(rollback_deployment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='add-note')
    def add_note(self, request, pk=None):
        """POST /api/v1/deployments/deployments/{id}/add-note/"""
        deployment = self.get_object()
        serializer = DeploymentNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(deployment=deployment, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """GET /api/v1/deployments/deployments/recent/ — last 20 deployments across all services."""
        recent = self.get_queryset().order_by('-triggered_at')[:20]
        return Response(DeploymentSerializer(recent, many=True).data)
