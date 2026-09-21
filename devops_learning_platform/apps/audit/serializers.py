from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            'id', 'username_snapshot', 'action', 'resource_type', 'resource_id',
            'description', 'method', 'path', 'ip_address', 'user_agent',
            'status_code', 'request_data', 'changes', 'timestamp',
        ]
        read_only_fields = fields  # Audit logs are immutable via API
