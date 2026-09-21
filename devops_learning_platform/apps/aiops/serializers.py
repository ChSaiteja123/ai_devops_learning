from rest_framework import serializers
from .models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    approved_by_username = serializers.ReadOnlyField(source='approved_by.username')

    class Meta:
        model = Incident
        fields = [
            'id', 'title', 'severity', 'status', 'description',
            'metrics_snapshot', 'root_cause', 'evidence', 'impact',
            'recommendation', 'confidence_score', 'suggested_remediation',
            'requires_human_approval', 'approved_by_username', 'approved_at',
            'source', 'created_at', 'resolved_at',
        ]
        read_only_fields = [
            'root_cause', 'evidence', 'impact', 'recommendation',
            'confidence_score', 'approved_by_username', 'approved_at', 'created_at',
        ]


class AnalyzeInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    metrics = serializers.DictField()
    logs = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    context = serializers.DictField(required=False, default=dict)


class ApproveRemediationSerializer(serializers.Serializer):
    approved = serializers.BooleanField()
    notes = serializers.CharField(required=False, allow_blank=True)
