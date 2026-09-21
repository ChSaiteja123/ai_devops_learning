"""
Notifications Models.

WHY NOTIFICATIONS MATTER:
--------------------------
Users need to know when important things happen:
  - 🏆 "You earned a certificate!" (course completed)
  - 🚨 "Critical incident detected in production" (AIOps alert)
  - 🚀 "Deployment to production succeeded"
  - 💬 "New reply on your question"
  - ⚠️  "Your lab submission is being reviewed"

This app provides an in-app notification system with:
  - Typed notifications (achievement, alert, deployment, system, etc.)
  - Read/unread state
  - Optional deep-link URL
  - Bulk mark-as-read
"""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """An in-app notification for a user."""

    TYPE_CHOICES = [
        ('achievement',  '🏆 Achievement'),
        ('alert',        '🚨 Alert'),
        ('deployment',   '🚀 Deployment'),
        ('system',       '⚙️  System'),
        ('course',       '📚 Course Update'),
        ('quiz',         '📝 Quiz'),
        ('lab',          '🔬 Lab'),
        ('project',      '🛠️  Project'),
        ('info',         'ℹ️  Info'),
    ]

    PRIORITY_CHOICES = [
        ('low',      'Low'),
        ('normal',   'Normal'),
        ('high',     'High'),
        ('critical', 'Critical'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')

    title = models.CharField(max_length=255)
    message = models.TextField()

    # Optional deep-link into the platform
    action_url = models.CharField(max_length=500, blank=True)
    action_label = models.CharField(max_length=100, blank=True)

    # Generic relation to the object that triggered this notification
    related_object_type = models.CharField(max_length=100, blank=True)
    related_object_id = models.CharField(max_length=64, blank=True)

    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', 'created_at']),
        ]

    def __str__(self):
        status = '✓' if self.is_read else '•'
        return f'[{status}] {self.recipient.username}: {self.title}'


class NotificationPreference(models.Model):
    """Per-user preferences for which notification types they want to receive."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
    )

    # Email notification toggles
    email_achievements = models.BooleanField(default=True)
    email_alerts = models.BooleanField(default=True)
    email_deployments = models.BooleanField(default=False)
    email_course_updates = models.BooleanField(default=True)
    email_system = models.BooleanField(default=True)

    # In-app toggles
    inapp_achievements = models.BooleanField(default=True)
    inapp_alerts = models.BooleanField(default=True)
    inapp_deployments = models.BooleanField(default=True)
    inapp_course_updates = models.BooleanField(default=True)
    inapp_system = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} notification preferences'
