"""
Notifications Views.

ENDPOINTS:
----------
GET    /api/v1/notifications/                         → List own notifications
POST   /api/v1/notifications/mark-read/               → Mark notifications as read
POST   /api/v1/notifications/mark-all-read/           → Mark ALL notifications as read
DELETE /api/v1/notifications/{id}/                    → Delete a single notification
GET    /api/v1/notifications/unread-count/            → Quick unread badge count
GET    /api/v1/notifications/preferences/             → Get notification preferences
PUT    /api/v1/notifications/preferences/             → Update notification preferences
"""
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer, MarkReadSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Read-only ViewSet for user notifications.
    Users can only see and delete their own.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user)
        # Optional ?unread=true filter
        if self.request.query_params.get('unread') == 'true':
            qs = qs.filter(is_read=False)
        # Optional ?type=alert filter
        ntype = self.request.query_params.get('type')
        if ntype:
            qs = qs.filter(notification_type=ntype)
        return qs

    def perform_destroy(self, instance):
        # Users can only delete their own notifications
        if instance.recipient != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You cannot delete another user\'s notification.')
        instance.delete()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_read(request):
    """
    POST /api/v1/notifications/mark-read/
    Body: {"ids": [1, 2, 3]}  — mark specific notifications as read.
    """
    serializer = MarkReadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ids = serializer.validated_data.get('ids', [])

    qs = Notification.objects.filter(recipient=request.user, is_read=False)
    if ids:
        qs = qs.filter(id__in=ids)

    count = qs.update(is_read=True, read_at=timezone.now())
    return Response({'marked_read': count})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_read(request):
    """POST /api/v1/notifications/mark-all-read/"""
    count = Notification.objects.filter(
        recipient=request.user, is_read=False
    ).update(is_read=True, read_at=timezone.now())
    return Response({'marked_read': count})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_count(request):
    """GET /api/v1/notifications/unread-count/ — lightweight badge count."""
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return Response({'unread_count': count})


class NotificationPreferenceView(APIView):
    """
    GET  /api/v1/notifications/preferences/  → Retrieve preferences
    PUT  /api/v1/notifications/preferences/  → Full update
    PATCH /api/v1/notifications/preferences/ → Partial update
    """
    permission_classes = [permissions.IsAuthenticated]

    def _get_or_create(self, user):
        prefs, _ = NotificationPreference.objects.get_or_create(user=user)
        return prefs

    def get(self, request):
        prefs = self._get_or_create(request.user)
        return Response(NotificationPreferenceSerializer(prefs).data)

    def put(self, request):
        return self._update(request, partial=False)

    def patch(self, request):
        return self._update(request, partial=True)

    def _update(self, request, partial):
        prefs = self._get_or_create(request.user)
        serializer = NotificationPreferenceSerializer(prefs, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
