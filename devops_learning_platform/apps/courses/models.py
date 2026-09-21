"""
Courses Models.

DATA MODEL DESIGN:
------------------
Category (1) ──< Course (many)
Course (1) ──< Lesson (many)
Course (1) ──< Quiz (many)
Course (1) ──< Lab (many)

This is a one-to-many relationship.
ForeignKey creates the "many" side.

LEARNING: Course Categories
----------------------------
Each course belongs to a technology category:
  - Python / Django
  - Docker / Containers
  - Kubernetes
  - AWS
  - Terraform
  - CI/CD
  - Monitoring
  - AI Engineering
  - DevSecOps
"""
from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    """Technology category (Docker, Kubernetes, AWS, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50, blank=True,
        help_text='FontAwesome icon class, e.g. fa-docker'
    )
    color = models.CharField(
        max_length=20, blank=True, default='#3B82F6',
        help_text='Hex color for UI badges'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    A course is a collection of lessons on one technology.
    Example: "Complete Docker Course" with 20 lessons.
    """
    DIFFICULTY_CHOICES = [
        ('beginner', '🟢 Beginner'),
        ('intermediate', '🟡 Intermediate'),
        ('advanced', '🔴 Advanced'),
    ]
    LEVEL_CHOICES = [
        ('level1', 'Level 1 — Beginner'),
        ('level2', 'Level 2 — Intermediate'),
        ('level3', 'Level 3 — Advanced DevOps'),
        ('level4', 'Level 4 — Production'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses'
    )
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    platform_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='level1')
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    preview_video_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    estimated_duration_hours = models.DecimalField(max_digits=5, decimal_places=1, default=1.0)

    # What learners will gain
    what_you_learn = models.JSONField(
        default=list,
        help_text='List of learning outcomes, e.g. ["Deploy on Kubernetes", "Use Helm"]'
    )
    prerequisites = models.JSONField(
        default=list,
        help_text='List of prerequisite knowledge strings'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def lesson_count(self):
        return self.lessons.count()

    @property
    def enrolled_count(self):
        from apps.progress.models import Enrollment
        return Enrollment.objects.filter(course=self).count()
