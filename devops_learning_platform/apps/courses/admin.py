from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Course


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_badge', 'icon', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']
    ordering = ['order']

    def color_badge(self, obj):
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:4px">{}</span>',
            obj.color, obj.color
        )
    color_badge.short_description = 'Color'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'platform_level', 'is_published', 'is_featured', 'lesson_count', 'enrolled_count']
    list_filter = ['difficulty', 'platform_level', 'is_published', 'is_featured', 'category']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'is_featured']
    filter_horizontal = []
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'slug', 'category', 'difficulty', 'platform_level', 'short_description', 'description')}),
        ('Media', {'fields': ('thumbnail', 'preview_video_url')}),
        ('Content', {'fields': ('what_you_learn', 'prerequisites', 'estimated_duration_hours')}),
        ('Status', {'fields': ('is_published', 'is_featured', 'order')}),
    )

    def lesson_count(self, obj):
        return obj.lesson_count
    lesson_count.short_description = '📚 Lessons'

    def enrolled_count(self, obj):
        return obj.enrolled_count
    enrolled_count.short_description = '👥 Enrolled'
