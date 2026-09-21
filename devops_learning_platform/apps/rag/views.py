from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Document, RAGQuery
from .serializers import (
    DocumentSerializer, DocumentUploadSerializer,
    RAGQueryInputSerializer, RAGQueryResultSerializer
)
from .services import RAGService


class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(uploaded_by=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentUploadSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        doc = serializer.save(uploaded_by=self.request.user)
        # Trigger background indexing
        try:
            from .tasks import index_document_task
            index_document_task.delay(doc.id)
        except Exception:
            # If Celery not available, index synchronously
            service = RAGService()
            service.index_document(doc)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def query_knowledge_base(request):
    """
    POST /api/v1/rag/query/

    Body: {"query": "How do I set up Kubernetes RBAC?", "category": "kubernetes"}
    Returns: {answer, sources, confidence, response_time_ms}
    """
    serializer = RAGQueryInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    service = RAGService()
    result = service.query(
        query_text=serializer.validated_data['query'],
        user=request.user,
        n_results=serializer.validated_data.get('n_results', 5),
    )
    return Response(result)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def query_history(request):
    """GET /api/v1/rag/history/ — user's query history"""
    queries = RAGQuery.objects.filter(user=request.user)[:50]
    return Response(RAGQueryResultSerializer(queries, many=True).data)
