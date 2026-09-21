from django.db import models
from apps.courses.models import Course


class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('video', '🎥 Video'),
        ('text', '📝 Text/Article'),
        ('interactive', '💻 Interactive'),
        ('lab', '🔬 Lab'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='text')
    content = models.TextField(help_text='Markdown content for the lesson body')
    video_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=0)
    is_free_preview = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    # Architecture diagram embedded in lesson (Mermaid syntax)
    architecture_diagram = models.TextField(
        blank=True,
        help_text='Mermaid.js diagram code to embed in this lesson'
    )

    # Learning objectives for this specific lesson
    objectives = models.JSONField(default=list)

    # Commands to run for this lesson (for lab-type lessons)
    commands = models.JSONField(
        default=list,
        help_text='List of {command, explanation, expected_output} objects'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.course.title} — {self.order}. {self.title}'
