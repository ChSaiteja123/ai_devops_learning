from django.contrib import admin
from .models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'severity', 'status', 'confidence_score',
        'requires_human_approval', 'approved_by', 'source', 'created_at',
    ]
    list_filter = ['severity', 'status', 'requires_human_approval', 'source']
    search_fields = ['title', 'description', 'root_cause']
    readonly_fields = ['created_at', 'approved_at']
    ordering = ['-created_at']
    fieldsets = (
        ('Incident Details', {
            'fields': ('title', 'severity', 'status', 'description', 'source'),
        }),
        ('Metrics', {
            'fields': ('metrics_snapshot',),
        }),
        ('AI Analysis', {
            'fields': (
                'root_cause', 'evidence', 'impact', 'recommendation',
                'confidence_score', 'suggested_remediation',
            ),
        }),
        ('Human Approval', {
            'fields': ('requires_human_approval', 'approved_by', 'approved_at'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'resolved_at'),
        }),
    )
