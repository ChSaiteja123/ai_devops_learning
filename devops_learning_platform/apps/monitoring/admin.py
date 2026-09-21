from django.contrib import admin
from .models import MetricSnapshot, AlertRule, Alert, HealthCheck


@admin.register(MetricSnapshot)
class MetricSnapshotAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'source', 'namespace', 'cpu_percent', 'memory_percent', 'error_rate', 'recorded_at']
    list_filter = ['source', 'service_name']
    search_fields = ['service_name', 'namespace']
    ordering = ['-recorded_at']


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'metric', 'operator', 'threshold', 'severity', 'is_active', 'service_name']
    list_filter = ['severity', 'is_active', 'metric']
    search_fields = ['name', 'service_name']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['rule', 'service_name', 'severity', 'status', 'metric_value', 'fired_at', 'resolved_at']
    list_filter = ['status', 'severity', 'service_name']
    search_fields = ['service_name', 'message']
    ordering = ['-fired_at']


@admin.register(HealthCheck)
class HealthCheckAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'endpoint', 'status', 'response_time_ms', 'status_code', 'checked_at']
    list_filter = ['status', 'service_name']
    search_fields = ['service_name', 'endpoint']
    ordering = ['-checked_at']
