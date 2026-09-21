from rest_framework import serializers
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'priority', 'title', 'message',
            'action_url', 'action_label',
            'related_object_type', 'related_object_id',
            'is_read', 'read_at', 'created_at',
        ]
        read_only_fields = ['read_at', 'created_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            'email_achievements', 'email_alerts', 'email_deployments',
            'email_course_updates', 'email_system',
            'inapp_achievements', 'inapp_alerts', 'inapp_deployments',
            'inapp_course_updates', 'inapp_system',
            'updated_at',
        ]
        read_only_fields = ['updated_at']


class MarkReadSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text='List of notification IDs to mark as read. Omit to mark all as read.',
    )
