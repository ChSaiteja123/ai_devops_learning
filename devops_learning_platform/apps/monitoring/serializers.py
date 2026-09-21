from rest_framework import serializers
from .models import MetricSnapshot, AlertRule, Alert, HealthCheck


class MetricSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricSnapshot
        fields = [
            'id', 'source', 'service_name', 'namespace',
            'cpu_percent', 'memory_percent', 'request_rate', 'error_rate',
            'latency_p50_ms', 'latency_p99_ms', 'pod_count', 'pod_restarts',
            'raw_metrics', 'recorded_at',
        ]
        read_only_fields = ['recorded_at']


class AlertRuleSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = AlertRule
        fields = [
            'id', 'name', 'description', 'service_name', 'metric',
            'operator', 'threshold', 'severity', 'is_active',
            'created_by_username', 'created_at',
        ]
        read_only_fields = ['created_by_username', 'created_at']


class AlertSerializer(serializers.ModelSerializer):
    rule_name = serializers.ReadOnlyField(source='rule.name')
    acknowledged_by_username = serializers.ReadOnlyField(source='acknowledged_by.username')

    class Meta:
        model = Alert
        fields = [
            'id', 'rule', 'rule_name', 'service_name', 'severity', 'status',
            'message', 'metric_value', 'labels', 'annotations',
            'fired_at', 'resolved_at', 'acknowledged_by_username',
        ]
        read_only_fields = ['fired_at', 'rule_name', 'acknowledged_by_username']


class HealthCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCheck
        fields = [
            'id', 'service_name', 'endpoint', 'status',
            'response_time_ms', 'status_code', 'error_message', 'checked_at',
        ]
        read_only_fields = ['checked_at']
