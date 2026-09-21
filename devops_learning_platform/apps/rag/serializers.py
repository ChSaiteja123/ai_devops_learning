from rest_framework import serializers
from .models import Document, RAGQuery


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'source_type', 'category', 'file', 'url',
            'chunk_count', 'status', 'error_message', 'created_at', 'indexed_at',
        ]
        read_only_fields = ['chunk_count', 'status', 'error_message', 'created_at', 'indexed_at']


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['title', 'category', 'file', 'url', 'content']

    def validate(self, attrs):
        if not attrs.get('file') and not attrs.get('url') and not attrs.get('content'):
            raise serializers.ValidationError('Provide a file, URL, or text content.')
        return attrs


class RAGQueryInputSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=2000)
    category = serializers.CharField(required=False, allow_blank=True)
    n_results = serializers.IntegerField(default=5, min_value=1, max_value=20)


class RAGQueryResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAGQuery
        fields = ['id', 'query', 'answer', 'source_documents', 'confidence_score', 'response_time_ms', 'created_at']
