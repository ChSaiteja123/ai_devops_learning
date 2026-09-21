from django.contrib import admin
from .models import Lab, LabSubmission


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ['title', 'technology', 'difficulty', 'estimated_minutes', 'is_published', 'order']
    list_filter = ['technology', 'difficulty', 'is_published']
    search_fields = ['title', 'objective']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'order']


@admin.register(LabSubmission)
class LabSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'lab', 'completed_at', 'time_taken_minutes']
    list_filter = ['lab__technology', 'completed_at']
    readonly_fields = ['completed_at']
