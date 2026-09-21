from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, ProjectSubmission
from .serializers import ProjectSerializer, ProjectSubmissionSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_published=True)
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def submit(self, request, pk=None):
        project = self.get_object()
        data = {**request.data, 'project': project.id}
        serializer = ProjectSubmissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            from apps.progress.models import UserProgress
            UserProgress.objects.get_or_create(
                user=request.user, content_type='project', object_id=project.id,
                defaults={'completed': True, 'points_earned': 50}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
