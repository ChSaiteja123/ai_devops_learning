from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content_type', 'order', 'duration_minutes', 'is_published', 'is_free_preview']
    list_filter = ['content_type', 'is_published', 'is_free_preview', 'course__category']
    search_fields = ['title', 'course__title', 'content']
    list_editable = ['order', 'is_published', 'is_free_preview']
    prepopulated_fields = {'slug': ('title',)}
    list_select_related = ['course']
    fieldsets = (
        ('Basic', {'fields': ('course', 'title', 'slug', 'content_type', 'order')}),
        ('Content', {'fields': ('content', 'video_url', 'duration_minutes', 'architecture_diagram')}),
        ('Learning', {'fields': ('objectives', 'commands')}),
        ('Status', {'fields': ('is_published', 'is_free_preview')}),
    )
