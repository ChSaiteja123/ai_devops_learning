"""
AIOps Views.

ENDPOINTS:
----------
GET  /api/v1/aiops/incidents/                          → List all incidents
POST /api/v1/aiops/incidents/                          → Create a bare incident record
GET  /api/v1/aiops/incidents/{id}/                     → Detail of one incident
POST /api/v1/aiops/analyze/                            → Analyze metrics → create incident with AI result
POST /api/v1/aiops/incidents/{id}/approve/             → Human approves suggested remediation
POST /api/v1/aiops/incidents/{id}/resolve/             → Mark incident as resolved
GET  /api/v1/aiops/incidents/open/                     → All open/analyzing incidents

SAFETY NOTE:
------------
The AI NEVER takes automated action. It only produces recommendations.
A human MUST approve before any remediation happens (requires_human_approval=True always).
"""
import logging
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .models import Incident
from .serializers import IncidentSerializer, AnalyzeInputSerializer, ApproveRemediationSerializer
from .services import AIOpsAnalyzer

logger = logging.getLogger(__name__)


class IncidentViewSet(viewsets.ModelViewSet):
    """
    CRUD for Incident records.
    Read: any authenticated user.
    Write (create/update/delete): staff only.
    Special actions: analyze, approve, resolve — authenticated users.
    """
    queryset = Incident.objects.select_related('approved_by').all()
    serializer_class = IncidentSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def open(self, request):
        """GET /api/v1/aiops/incidents/open/ — incidents that need attention."""
        qs = Incident.objects.filter(status__in=['open', 'analyzing']).order_by('-created_at')
        return Response(IncidentSerializer(qs, many=True).data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        POST /api/v1/aiops/incidents/{id}/approve/
        Human reviews and approves (or rejects) the AI's remediation suggestion.

        Body: {"approved": true, "notes": "Looks good, proceeding."}
        """
        incident = self.get_object()

        if not incident.requires_human_approval:
            return Response(
                {'detail': 'This incident does not require human approval.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ApproveRemediationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        approved = serializer.validated_data['approved']
        notes = serializer.validated_data.get('notes', '')

        incident.approved_by = request.user
        incident.approved_at = timezone.now()
        incident.requires_human_approval = False

        if approved:
            incident.status = 'analyzing'
            if notes:
                incident.recommendation = f'{incident.recommendation}\n\n✅ Approved by {request.user.username}: {notes}'
        else:
            incident.status = 'suppressed'
            if notes:
                incident.recommendation = f'{incident.recommendation}\n\n❌ Rejected by {request.user.username}: {notes}'

        incident.save()
        return Response(IncidentSerializer(incident).data)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """POST /api/v1/aiops/incidents/{id}/resolve/ — mark incident as resolved."""
        incident = self.get_object()
        if incident.status == 'resolved':
            return Response({'detail': 'Incident is already resolved.'}, status=status.HTTP_400_BAD_REQUEST)
        incident.status = 'resolved'
        incident.resolved_at = timezone.now()
        incident.save(update_fields=['status', 'resolved_at'])
        return Response(IncidentSerializer(incident).data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def analyze(request):
    """
    POST /api/v1/aiops/analyze/

    Submit metrics (and optionally logs + context) for AI analysis.
    Creates an Incident record with the analysis results attached.

    Request body:
    {
        "title": "High CPU on api-server",
        "metrics": {"cpu_percent": 95, "memory_percent": 72, "error_rate": 0.02},
        "logs": ["ERROR: timeout after 30s", "WARN: connection pool exhausted"],
        "context": {"recent_deployment": "v2.4.1 deployed 10 mins ago"}
    }
    """
    serializer = AnalyzeInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    title = serializer.validated_data['title']
    metrics = serializer.validated_data['metrics']
    logs = serializer.validated_data.get('logs', [])
    context = serializer.validated_data.get('context', {})

    # Run analysis (AI with rule-based fallback)
    analyzer = AIOpsAnalyzer()
    try:
        result = analyzer.analyze(metrics=metrics, logs=logs, context=context)
    except Exception as exc:
        logger.error('AIOps analysis failed: %s', exc, exc_info=True)
        return Response(
            {'detail': f'Analysis failed: {exc}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Create the incident record with analysis results
    incident = Incident.objects.create(
        title=title,
        severity=result.get('severity', 'medium'),
        status='analyzing',
        description=f'Auto-detected incident. Analysis method: {result.get("analysis_method", "unknown")}',
        metrics_snapshot=metrics,
        root_cause=result.get('root_cause', ''),
        evidence=result.get('evidence', []),
        impact=result.get('impact', ''),
        recommendation=result.get('recommendation', ''),
        confidence_score=result.get('confidence', 0.0),
        suggested_remediation=result.get('suggested_remediation', ''),
        requires_human_approval=result.get('requires_human_approval', True),
        source='api',
    )

    return Response(
        {
            'incident': IncidentSerializer(incident).data,
            'analysis': result,
        },
        status=status.HTTP_201_CREATED,
    )
