from rest_framework import serializers
from .models import Project, ProjectSubmission


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'number', 'title', 'slug', 'tech_stack', 'description',
            'objectives', 'steps', 'architecture_diagram', 'github_template_url',
            'estimated_hours', 'is_published',
        ]


class ProjectSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSubmission
        fields = ['id', 'project', 'github_url', 'notes', 'submitted_at', 'is_reviewed']
        read_only_fields = ['submitted_at', 'is_reviewed']
