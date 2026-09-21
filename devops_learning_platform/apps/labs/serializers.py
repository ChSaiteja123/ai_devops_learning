from rest_framework import serializers
from .models import Lab, LabSubmission


class LabListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['id', 'title', 'slug', 'technology', 'difficulty', 'objective', 'estimated_minutes']


class LabDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = [
            'id', 'course', 'title', 'slug', 'technology', 'difficulty',
            'objective', 'prerequisites', 'estimated_minutes', 'steps',
            'common_errors', 'interview_questions', 'created_at',
        ]


class LabSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabSubmission
        fields = ['id', 'lab', 'completed_at', 'notes', 'time_taken_minutes']
        read_only_fields = ['completed_at']
