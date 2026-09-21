from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'username_snapshot', 'action', 'resource_type', 'resource_id', 'method', 'status_code', 'ip_address']
    list_filter = ['action', 'resource_type', 'status_code']
    search_fields = ['username_snapshot', 'path', 'description', 'ip_address']
    readonly_fields = [f.name for f in AuditLog._meta.fields]
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False  # Audit logs are created only by middleware

    def has_change_permission(self, request, obj=None):
        return False  # Immutable

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can purge old logs
