from django.db import models
from apps.courses.models import Course


class Lab(models.Model):
    """Hands-on lab with step-by-step instructions."""
    TECH_CHOICES = [
        ('docker', 'Docker'), ('kubernetes', 'Kubernetes'), ('aws', 'AWS'),
        ('terraform', 'Terraform'), ('jenkins', 'Jenkins'), ('git', 'Git'),
        ('python', 'Python'), ('django', 'Django'), ('prometheus', 'Prometheus'),
        ('grafana', 'Grafana'), ('argocd', 'Argo CD'), ('helm', 'Helm'),
        ('linux', 'Linux'), ('ai', 'AI Engineering'),
    ]
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'),
    ]

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='labs')
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    technology = models.CharField(max_length=30, choices=TECH_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    objective = models.TextField(help_text='What the learner will accomplish')
    prerequisites = models.JSONField(default=list)
    estimated_minutes = models.PositiveIntegerField(default=30)
    steps = models.JSONField(
        default=list,
        help_text='List of {step_number, title, description, command, expected_output} objects'
    )
    common_errors = models.JSONField(default=list, help_text='List of {error, cause, fix}')
    interview_questions = models.JSONField(default=list)
    is_published = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['technology', 'order']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.get_technology_display()}] {self.title}'


class LabSubmission(models.Model):
    """Tracks when a user completes a lab."""
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='lab_submissions')
    completed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    time_taken_minutes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['lab', 'user']

    def __str__(self):
        return f'{self.user.username} completed {self.lab.title}'
