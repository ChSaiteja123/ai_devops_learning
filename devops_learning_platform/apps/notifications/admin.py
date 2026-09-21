from django.contrib import admin
from .models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'priority', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read']
    search_fields = ['recipient__username', 'title', 'message']
    ordering = ['-created_at']
    readonly_fields = ['read_at', 'created_at']


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_achievements', 'email_alerts', 'inapp_alerts', 'updated_at']
    search_fields = ['user__username']
