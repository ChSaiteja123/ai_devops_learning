from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotificationViewSet, mark_read, mark_all_read,
    unread_count, NotificationPreferenceView,
)

router = DefaultRouter()
router.register('', NotificationViewSet, basename='notification')

urlpatterns = [
    path('mark-read/', mark_read, name='notification-mark-read'),
    path('mark-all-read/', mark_all_read, name='notification-mark-all-read'),
    path('unread-count/', unread_count, name='notification-unread-count'),
    path('preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
    path('', include(router.urls)),
]
