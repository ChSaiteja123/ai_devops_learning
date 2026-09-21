from django.db import models
from django.conf import settings


class Incident(models.Model):
    """AIOps-detected or manually reported incident."""
    SEVERITY_CHOICES = [
        ('critical', '🔴 Critical'), ('high', '🟠 High'),
        ('medium', '🟡 Medium'), ('low', '🟢 Low'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'), ('analyzing', 'Analyzing'), ('resolved', 'Resolved'),
        ('suppressed', 'Suppressed'),
    ]

    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    description = models.TextField()

    # Raw metrics at time of incident
    metrics_snapshot = models.JSONField(default=dict)

    # AI analysis result
    root_cause = models.TextField(blank=True)
    evidence = models.JSONField(default=list)
    impact = models.TextField(blank=True)
    recommendation = models.TextField(blank=True)
    confidence_score = models.FloatField(default=0.0)
    suggested_remediation = models.TextField(blank=True)

    # Human approval gate — NEVER auto-remediate without this
    requires_human_approval = models.BooleanField(default=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='approved_incidents'
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    source = models.CharField(max_length=50, default='prometheus', help_text='alertmanager, manual, etc.')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.severity.upper()}] {self.title}'
