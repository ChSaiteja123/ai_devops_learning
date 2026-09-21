from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ArchitectureDiagram
from .serializers import ArchitectureDiagramSerializer
from .generators import ArchitectureGenerator


class ArchitectureDiagramViewSet(viewsets.ModelViewSet):
    serializer_class = ArchitectureDiagramSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if settings.DEBUG and self.action in {'generate', 'demo_generate'}:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        return ArchitectureDiagram.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['post'])
    def generate(self, request):
        prompt = request.data.get('prompt', '')
        provider = request.data.get('cloud_provider', 'aws')
        generator = ArchitectureGenerator()
        result = generator.generate(prompt=prompt, cloud_provider=provider)
        return Response(result)

    @action(detail=False, methods=['post'], url_path='demo-generate')
    def demo_generate(self, request):
        prompt = request.data.get('prompt', 'A simple AWS web app with ALB, EC2, and RDS')
        provider = request.data.get('cloud_provider', 'aws')
        generator = ArchitectureGenerator()
        return Response(generator.generate(prompt=prompt, cloud_provider=provider))
