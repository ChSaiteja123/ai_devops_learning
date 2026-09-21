from django.db import models
from django.conf import settings


class ArchitectureDiagram(models.Model):
    CLOUD_PROVIDER_CHOICES = [
        ('aws', 'AWS'),
        ('gcp', 'GCP'),
        ('azure', 'Azure'),
        ('multi', 'Multi-Cloud'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diagrams')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cloud_provider = models.CharField(max_length=10, choices=CLOUD_PROVIDER_CHOICES, default='aws')
    diagram_data = models.JSONField(default=dict)
    diagram_image = models.ImageField(upload_to='diagrams/', blank=True, null=True)
    prompt_used = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
