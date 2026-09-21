"""
Audit Log Models.

WHAT IS AN AUDIT LOG?
---------------------
An audit log records every significant action taken in the system:
  - Who did it (user)
  - What they did (action: CREATE, UPDATE, DELETE, VIEW)
  - What was affected (resource type + id)
  - When it happened (timestamp)
  - Where the request came from (IP address, user agent)

Audit logs are required for:
  - Security compliance (SOC 2, PCI-DSS, HIPAA)
  - Incident investigation ("who deleted that record?")
  - User behaviour analytics
"""
from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """Records every significant API action for security and compliance."""

    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('VIEW',   'View'),
        ('LOGIN',  'Login'),
        ('LOGOUT', 'Logout'),
        ('FAILED_LOGIN', 'Failed Login'),
        ('PASSWORD_CHANGE', 'Password Change'),
        ('EXPORT', 'Export'),
    ]

    # Who — null for anonymous/unauthenticated requests
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='audit_logs',
    )
    username_snapshot = models.CharField(
        max_length=150, blank=True,
        help_text='Username at time of action (preserved if user is deleted)',
    )

    # What
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource_type = models.CharField(
        max_length=100, blank=True,
        help_text='e.g. Course, Lab, Incident',
    )
    resource_id = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)

    # Request metadata
    method = models.CharField(max_length=10, blank=True)   # GET, POST, etc.
    path = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    # Response
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)

    # Payload snapshot (redacted sensitive fields)
    request_data = models.JSONField(default=dict, blank=True)
    changes = models.JSONField(
        default=dict, blank=True,
        help_text='Before/after values for UPDATE actions',
    )

    # When
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['resource_type', 'resource_id']),
            models.Index(fields=['action', 'timestamp']),
        ]

    def __str__(self):
        return f'[{self.timestamp:%Y-%m-%d %H:%M}] {self.username_snapshot or "anon"} {self.action} {self.resource_type}'
