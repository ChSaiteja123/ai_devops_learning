"""
Monitoring Models.

WHAT IS OBSERVABILITY?
----------------------
Observability is the ability to understand the internal state of a system
from its external outputs. The three pillars are:

  1. Metrics    — Numerical measurements over time (CPU %, request rate)
  2. Logs       — Timestamped text records of events
  3. Traces     — End-to-end path of a single request through microservices

This app tracks:
  - MetricSnapshot : point-in-time metric readings from Prometheus/k8s
  - AlertRule      : defines when to trigger an alert (threshold-based)
  - Alert          : a fired alert instance
  - HealthCheck    : periodic checks on service endpoints
"""
from django.db import models
from django.conf import settings


class MetricSnapshot(models.Model):
    """A point-in-time snapshot of system metrics."""

    SOURCE_CHOICES = [
        ('prometheus', 'Prometheus'),
        ('kubernetes', 'Kubernetes'),
        ('cloudwatch', 'AWS CloudWatch'),
        ('custom',     'Custom'),
    ]

    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='prometheus')
    service_name = models.CharField(max_length=100)
    namespace = models.CharField(max_length=100, blank=True, help_text='K8s namespace or AWS region')

    # Core metrics — stored individually for easy querying
    cpu_percent = models.FloatField(null=True, blank=True)
    memory_percent = models.FloatField(null=True, blank=True)
    request_rate = models.FloatField(null=True, blank=True, help_text='Requests per second')
    error_rate = models.FloatField(null=True, blank=True, help_text='Error rate 0.0–1.0')
    latency_p50_ms = models.FloatField(null=True, blank=True)
    latency_p99_ms = models.FloatField(null=True, blank=True)
    pod_count = models.PositiveIntegerField(null=True, blank=True)
    pod_restarts = models.PositiveIntegerField(null=True, blank=True)

    # Full raw payload for additional metrics
    raw_metrics = models.JSONField(default=dict)

    recorded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['service_name', 'recorded_at']),
        ]

    def __str__(self):
        return f'{self.service_name} @ {self.recorded_at:%Y-%m-%d %H:%M}'


class AlertRule(models.Model):
    """Defines a threshold-based alerting rule."""

    SEVERITY_CHOICES = [
        ('critical', '🔴 Critical'),
        ('warning',  '🟡 Warning'),
        ('info',     '🔵 Info'),
    ]
    METRIC_CHOICES = [
        ('cpu_percent',    'CPU %'),
        ('memory_percent', 'Memory %'),
        ('error_rate',     'Error Rate'),
        ('latency_p99_ms', 'P99 Latency (ms)'),
        ('pod_restarts',   'Pod Restarts'),
        ('request_rate',   'Request Rate (rps)'),
    ]
    OPERATOR_CHOICES = [
        ('gt', '>'), ('gte', '>='), ('lt', '<'), ('lte', '<='), ('eq', '=='),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    service_name = models.CharField(max_length=100, blank=True, help_text='Leave blank to apply to all services')
    metric = models.CharField(max_length=50, choices=METRIC_CHOICES)
    operator = models.CharField(max_length=5, choices=OPERATOR_CHOICES, default='gt')
    threshold = models.FloatField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='warning')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='alert_rules',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.metric} {self.operator} {self.threshold})'

    def evaluate(self, value: float) -> bool:
        """Return True if the rule fires for a given metric value."""
        ops = {
            'gt':  lambda v, t: v > t,
            'gte': lambda v, t: v >= t,
            'lt':  lambda v, t: v < t,
            'lte': lambda v, t: v <= t,
            'eq':  lambda v, t: v == t,
        }
        return ops[self.operator](value, self.threshold)


class Alert(models.Model):
    """A fired alert instance triggered by an AlertRule."""

    STATUS_CHOICES = [
        ('firing',    '🔴 Firing'),
        ('resolved',  '✅ Resolved'),
        ('silenced',  '🔕 Silenced'),
        ('pending',   '⏳ Pending'),
    ]

    rule = models.ForeignKey(AlertRule, on_delete=models.CASCADE, related_name='alerts')
    service_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='firing')
    message = models.TextField()
    metric_value = models.FloatField()
    labels = models.JSONField(default=dict, help_text='Prometheus-style labels')
    annotations = models.JSONField(default=dict)

    fired_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='acknowledged_alerts',
    )

    class Meta:
        ordering = ['-fired_at']

    def __str__(self):
        return f'[{self.severity.upper()}] {self.rule.name} — {self.status}'


class HealthCheck(models.Model):
    """Periodic health-check results for service endpoints."""

    STATUS_CHOICES = [
        ('healthy',   '✅ Healthy'),
        ('degraded',  '⚠️ Degraded'),
        ('unhealthy', '❌ Unhealthy'),
        ('unknown',   '❓ Unknown'),
    ]

    service_name = models.CharField(max_length=100)
    endpoint = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unknown')
    response_time_ms = models.FloatField(null=True, blank=True)
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-checked_at']
        get_latest_by = 'checked_at'

    def __str__(self):
        return f'{self.service_name} — {self.status} @ {self.checked_at:%H:%M}'
