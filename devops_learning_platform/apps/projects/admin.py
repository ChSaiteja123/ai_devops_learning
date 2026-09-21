from django.contrib import admin
from .models import Project, ProjectSubmission


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'tech_stack', 'estimated_hours', 'is_published']
    list_filter = ['tech_stack', 'is_published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    ordering = ['number']


@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'submitted_at', 'is_reviewed', 'github_url']
    list_filter = ['is_reviewed', 'submitted_at']
    list_editable = ['is_reviewed']
