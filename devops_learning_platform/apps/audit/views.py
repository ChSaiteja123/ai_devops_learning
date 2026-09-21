"""
Audit Log Views.

SECURITY: Only staff/admin users can read audit logs.
Nobody can create, update, or delete audit logs via the API —
they are write-once records created only by AuditMiddleware.
"""
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from .serializers import AuditLogSerializer


class IsAdminUser(permissions.BasePermission):
    """Allow access only to staff/admin users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/v1/audit/logs/           → List audit logs (staff only)
    GET /api/v1/audit/logs/{id}/      → Detail of single log entry

    Supports filtering by:
      ?action=CREATE
      ?resource_type=courses
      ?username_snapshot=alice
      ?search=<text>   (searches path, description, username_snapshot)
    """
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'resource_type', 'resource_id', 'username_snapshot', 'status_code']
    search_fields = ['path', 'description', 'username_snapshot', 'resource_type']
    ordering_fields = ['timestamp', 'action', 'status_code']
    ordering = ['-timestamp']
