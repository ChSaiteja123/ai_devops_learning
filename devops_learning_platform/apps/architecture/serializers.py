from rest_framework import serializers
from .models import ArchitectureDiagram


class ArchitectureDiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchitectureDiagram
        fields = ['id', 'owner', 'title', 'description', 'cloud_provider',
                  'diagram_data', 'diagram_image', 'prompt_used', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']
