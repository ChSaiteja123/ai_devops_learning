"""
Deployments Models.

WHAT IS DEPLOYMENT TRACKING?
------------------------------
Deployment tracking answers the question:
  "What version of what service is running in which environment, and when was it deployed?"

This is critical for:
  - Correlating incidents with recent deployments ("did the error rate spike after the deploy?")
  - Rollback decisions ("what was the previous stable version?")
  - Change management and compliance
  - MTTR (Mean Time To Recovery) measurement

DEPLOYMENT PIPELINE STAGES:
----------------------------
  triggered → building → testing → deploying → deployed → failed / rolled_back
"""
from django.db import models
from django.conf import settings


class Environment(models.Model):
    """A deployment target environment (dev, staging, production, etc.)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_production = models.BooleanField(default=False)
    url = models.URLField(blank=True, help_text='Base URL of the environment')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Service(models.Model):
    """A deployable service or application."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    repository_url = models.URLField(blank=True)
    tech_stack = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='owned_services',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Deployment(models.Model):
    """A single deployment event of a service to an environment."""

    STATUS_CHOICES = [
        ('triggered',   '⏳ Triggered'),
        ('building',    '🔨 Building'),
        ('testing',     '🧪 Testing'),
        ('deploying',   '🚀 Deploying'),
        ('deployed',    '✅ Deployed'),
        ('failed',      '❌ Failed'),
        ('rolled_back', '↩️  Rolled Back'),
        ('cancelled',   '🚫 Cancelled'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='deployments')
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='deployments')
    version = models.CharField(max_length=100, help_text='Git tag, semver, or commit SHA')
    git_commit = models.CharField(max_length=40, blank=True, help_text='Full 40-char git commit SHA')
    git_branch = models.CharField(max_length=200, blank=True)
    docker_image = models.CharField(max_length=500, blank=True, help_text='image:tag')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='triggered')

    # Who triggered the deployment
    triggered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='deployments',
    )

    # Metadata
    changelog = models.TextField(blank=True, help_text='What changed in this deployment')
    config_changes = models.JSONField(default=dict, help_text='Environment variable or config changes')
    pipeline_url = models.URLField(blank=True, help_text='Link to CI/CD pipeline run')

    # Timing
    triggered_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Rollback link
    rolled_back_from = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='rollbacks',
        help_text='If this is a rollback, points to the failed deployment',
    )

    error_log = models.TextField(blank=True)

    class Meta:
        ordering = ['-triggered_at']
        indexes = [
            models.Index(fields=['service', 'environment', 'triggered_at']),
        ]

    def __str__(self):
        return f'{self.service.name} v{self.version} → {self.environment.name} [{self.status}]'

    @property
    def duration_seconds(self):
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class DeploymentNote(models.Model):
    """Comments/notes added to a deployment by team members."""
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Note on {self.deployment} by {self.author.username}'
