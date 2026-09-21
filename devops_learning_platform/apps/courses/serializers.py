from rest_framework import serializers
from .models import Category, Course


class CategorySerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'course_count']

    def get_course_count(self, obj):
        return obj.courses.filter(is_published=True).count()


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    lesson_count = serializers.ReadOnlyField()
    enrolled_count = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description', 'category',
            'difficulty', 'platform_level', 'thumbnail', 'is_featured',
            'estimated_duration_hours', 'lesson_count', 'enrolled_count',
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    lesson_count = serializers.ReadOnlyField()
    enrolled_count = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'category', 'difficulty', 'platform_level', 'thumbnail',
            'preview_video_url', 'is_featured', 'estimated_duration_hours',
            'what_you_learn', 'prerequisites', 'lesson_count', 'enrolled_count',
            'created_at', 'updated_at',
        ]
