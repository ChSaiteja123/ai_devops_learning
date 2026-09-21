from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lesson
from .serializers import LessonListSerializer, LessonDetailSerializer


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Lesson.objects.filter(is_published=True).select_related('course')
        course_slug = self.request.query_params.get('course')
        if course_slug:
            qs = qs.filter(course__slug=course_slug)
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LessonDetailSerializer
        return LessonListSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def complete(self, request, pk=None):
        """POST /api/v1/lessons/{id}/complete/ — mark lesson as completed"""
        lesson = self.get_object()
        from apps.progress.models import UserProgress
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            content_type='lesson',
            object_id=lesson.id,
        )
        if not progress.completed:
            progress.completed = True
            progress.points_earned = 10
            progress.save()
        return Response({'status': 'completed', 'points_earned': 10})
