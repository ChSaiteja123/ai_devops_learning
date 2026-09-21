from django.db import models
from django.conf import settings


class Enrollment(models.Model):
    """Tracks which users are enrolled in which courses."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.user.username} → {self.course.title}'


class UserProgress(models.Model):
    """Tracks completion of individual items (lesson, lab, quiz, project)."""
    CONTENT_TYPE_CHOICES = [
        ('lesson', 'Lesson'), ('lab', 'Lab'), ('quiz', 'Quiz'), ('project', 'Project'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    object_id = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)
    # Nullable — only set when completed=True is saved; auto_now_add would
    # incorrectly stamp the record creation time even when completed=False.
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'content_type', 'object_id']

    def save(self, *args, **kwargs):
        from django.utils import timezone
        # Stamp completed_at the first time completed flips to True
        if self.completed and self.completed_at is None:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} — {self.content_type}:{self.object_id}'


class Certificate(models.Model):
    """Certificate awarded when a user completes a course."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.CharField(max_length=64, unique=True)

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            import uuid
            self.certificate_id = str(uuid.uuid4()).replace('-', '').upper()[:16]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} — {self.course.title} [{self.certificate_id}]'


class LearningStreak(models.Model):
    """Tracks daily learning streaks."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} streak: {self.current_streak} days'
