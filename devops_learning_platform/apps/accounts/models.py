"""
Accounts Models.

WHAT IS A DJANGO MODEL?
-----------------------
A Django model is a Python class that maps to a database table.
Each attribute is a database column.

Django handles:
  - Creating the table (migrations)
  - CRUD operations (ORM)
  - Relationships between tables

We extend Django's AbstractUser so we keep all built-in auth
features (login, password hashing, permissions) and add our own fields.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum


class User(AbstractUser):
    """
    Custom User model.

    WHY EXTEND AbstractUser?
    -------------------------
    Django's default User model only has: username, email, password, first_name, last_name.
    We need extra fields for our learning platform.

    Always define AUTH_USER_MODEL = 'accounts.User' in settings BEFORE
    running any migrations. Changing it later is very painful.
    """
    bio = models.TextField(
        blank=True,
        help_text='A short biography or description about yourself.'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='Profile picture.'
    )
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', '🟢 Beginner'),
            ('intermediate', '🟡 Intermediate'),
            ('advanced', '🔴 Advanced'),
        ],
        default='beginner',
        help_text='Your current skill level. This personalizes your learning path.'
    )
    github_username = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    is_premium = models.BooleanField(
        default=False,
        help_text='Premium users get access to advanced labs and AI features.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.username} ({self.get_skill_level_display()})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username

    @property
    def total_points(self):
        """Calculate total learning points across all activities."""
        from apps.progress.models import UserProgress
        return UserProgress.objects.filter(user=self).aggregate(
            total=Sum('points_earned')
        )['total'] or 0
