from django.db import models
from apps.courses.models import Course


class Project(models.Model):
    """15 progressive capstone projects."""
    TECH_STACK_CHOICES = [
        ('django', 'Django REST API'),
        ('docker', 'Docker'),
        ('celery', 'Django + Celery + Redis'),
        ('jenkins', 'Jenkins CI/CD'),
        ('aws', 'AWS Deployment'),
        ('terraform', 'Terraform'),
        ('kubernetes', 'Kubernetes'),
        ('helm', 'Helm'),
        ('argocd', 'Argo CD GitOps'),
        ('devsecops', 'DevSecOps Pipeline'),
        ('monitoring', 'Prometheus + Grafana'),
        ('otel', 'OpenTelemetry'),
        ('rag', 'RAG Assistant'),
        ('aiops', 'AIOps Analyzer'),
        ('fullstack', 'Complete Platform'),
    ]

    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    tech_stack = models.CharField(max_length=30, choices=TECH_STACK_CHOICES)
    description = models.TextField()
    objectives = models.JSONField(default=list)
    steps = models.JSONField(default=list)
    architecture_diagram = models.TextField(blank=True, help_text='Mermaid diagram code')
    github_template_url = models.URLField(blank=True)
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1, default=2.0)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Project {self.number}: {self.title}'


class ProjectSubmission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    github_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['project', 'user']
