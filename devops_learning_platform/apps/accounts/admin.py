"""
Accounts Admin.

DJANGO ADMIN — THE KILLER FEATURE
-----------------------------------
Django's admin interface auto-generates a full CRUD UI for your models.
Register a model and instantly get: list views, search, filters, detail pages.

Custom admin classes let you:
  - Control which fields are shown in lists
  - Add search and filter functionality
  - Group fields into sections
  - Add custom actions
  - Override save/delete behavior
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced admin for our custom User model."""

    # Columns shown in the list view
    list_display = [
        'username', 'email', 'full_name', 'skill_level_badge',
        'is_premium', 'total_points', 'date_joined', 'is_active'
    ]
    list_filter = ['skill_level', 'is_premium', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    list_per_page = 30

    # Detail page layout — add our custom fields to the existing UserAdmin fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('🧑 Profile', {
            'fields': (
                'bio', 'avatar', 'skill_level', 'github_username',
                'linkedin_url', 'website_url', 'location', 'years_of_experience',
            )
        }),
        ('💎 Platform', {
            'fields': ('is_premium',)
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Profile', {
            'fields': ('email', 'skill_level')
        }),
    )

    def skill_level_badge(self, obj):
        """Render a colored badge for skill level."""
        colors = {
            'beginner': '#28a745',
            'intermediate': '#ffc107',
            'advanced': '#dc3545',
        }
        color = colors.get(obj.skill_level, '#6c757d')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',
            color,
            obj.get_skill_level_display()
        )
    skill_level_badge.short_description = 'Skill Level'

    def total_points(self, obj):
        return obj.total_points
    total_points.short_description = '⭐ Points'
