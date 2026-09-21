from django.contrib import admin
from .models import Environment, Service, Deployment, DeploymentNote


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_production', 'url']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'tech_stack', 'is_active', 'owner']
    list_filter = ['is_active']
    search_fields = ['name', 'tech_stack']
    prepopulated_fields = {'slug': ('name',)}


class DeploymentNoteInline(admin.TabularInline):
    model = DeploymentNote
    extra = 0
    readonly_fields = ['author', 'created_at']


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ['service', 'environment', 'version', 'status', 'triggered_by', 'triggered_at', 'duration_seconds']
    list_filter = ['status', 'environment', 'service']
    search_fields = ['version', 'git_commit', 'git_branch', 'changelog']
    ordering = ['-triggered_at']
    readonly_fields = ['triggered_at', 'duration_seconds']
    inlines = [DeploymentNoteInline]
