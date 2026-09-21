from rest_framework import serializers
from .models import Lesson


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'slug', 'content_type', 'duration_minutes', 'order', 'is_free_preview']


class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'title', 'slug', 'content_type', 'content',
            'video_url', 'duration_minutes', 'order', 'is_free_preview',
            'architecture_diagram', 'objectives', 'commands',
            'created_at', 'updated_at',
        ]
