from rest_framework import serializers
from .models import Environment, Service, Deployment, DeploymentNote


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ['id', 'name', 'slug', 'description', 'is_production', 'url']


class ServiceSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'description', 'repository_url', 'tech_stack', 'is_active', 'owner_username']
        read_only_fields = ['owner_username']


class DeploymentNoteSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = DeploymentNote
        fields = ['id', 'author_username', 'content', 'created_at']
        read_only_fields = ['author_username', 'created_at']


class DeploymentSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    environment_name = serializers.ReadOnlyField(source='environment.name')
    triggered_by_username = serializers.ReadOnlyField(source='triggered_by.username')
    duration_seconds = serializers.ReadOnlyField()
    notes = DeploymentNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Deployment
        fields = [
            'id', 'service', 'service_name', 'environment', 'environment_name',
            'version', 'git_commit', 'git_branch', 'docker_image',
            'status', 'triggered_by_username', 'changelog', 'config_changes',
            'pipeline_url', 'triggered_at', 'started_at', 'completed_at',
            'duration_seconds', 'rolled_back_from', 'error_log', 'notes',
        ]
        read_only_fields = [
            'triggered_by_username', 'triggered_at', 'duration_seconds', 'notes',
        ]


class UpdateDeploymentStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[c[0] for c in Deployment.STATUS_CHOICES])
    error_log = serializers.CharField(required=False, allow_blank=True)
