from rest_framework import serializers
from .models import Enrollment, UserProgress, Certificate, LearningStreak


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')
    course_slug = serializers.ReadOnlyField(source='course.slug')

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'course_title', 'course_slug', 'enrolled_at', 'completed', 'completed_at']
        read_only_fields = ['enrolled_at', 'completed_at']


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'content_type', 'object_id', 'completed', 'points_earned', 'completed_at', 'created_at']
        read_only_fields = ['completed_at', 'created_at']


class CertificateSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Certificate
        fields = ['id', 'course', 'course_title', 'issued_at', 'certificate_id']


class LearningStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningStreak
        fields = ['current_streak', 'longest_streak', 'last_activity_date']
