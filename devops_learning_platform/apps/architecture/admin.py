from django.contrib import admin
from .models import ArchitectureDiagram


@admin.register(ArchitectureDiagram)
class ArchitectureDiagramAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'cloud_provider', 'created_at']
    list_filter = ['cloud_provider']
