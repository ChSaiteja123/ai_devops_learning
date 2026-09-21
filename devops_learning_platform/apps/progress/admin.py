from django.contrib import admin
from .models import Enrollment, UserProgress, Certificate, LearningStreak


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at', 'completed']
    list_filter = ['completed', 'enrolled_at']
    search_fields = ['user__username', 'course__title']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'completed', 'points_earned', 'completed_at']
    list_filter = ['content_type', 'completed']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'certificate_id', 'issued_at']
    readonly_fields = ['certificate_id', 'issued_at']


@admin.register(LearningStreak)
class LearningStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'last_activity_date']
