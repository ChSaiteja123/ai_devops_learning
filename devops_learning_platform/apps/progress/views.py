from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Enrollment, UserProgress, Certificate, LearningStreak
from .serializers import (
    EnrollmentSerializer, UserProgressSerializer,
    CertificateSerializer, LearningStreakSerializer
)


class EnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related('course')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CertificateSerializer

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user).select_related('course')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def learning_dashboard(request):
    """
    GET /api/v1/progress/dashboard/
    Full learning dashboard for the current user.
    """
    user = request.user
    progress_qs = UserProgress.objects.filter(user=user)

    by_type = {}
    for item in progress_qs:
        t = item.content_type
        if t not in by_type:
            by_type[t] = {'completed': 0, 'total': 0}
        by_type[t]['total'] += 1
        if item.completed:
            by_type[t]['completed'] += 1

    # Skills progress — completed lessons per category, correctly scoped
    from apps.courses.models import Category
    from apps.lessons.models import Lesson

    # Pre-fetch all lesson IDs the user has completed in a single query
    completed_lesson_ids = set(
        progress_qs.filter(content_type='lesson', completed=True)
        .values_list('object_id', flat=True)
    )

    skills = []
    for cat in Category.objects.all():
        # All published lesson IDs in this category
        category_lesson_ids = set(
            Lesson.objects.filter(
                course__category=cat,
                course__is_published=True,
                is_published=True,
            ).values_list('id', flat=True)
        )
        total_lessons = len(category_lesson_ids)
        # Intersection: lessons in this category that the user completed
        completed_in_cat = len(completed_lesson_ids & category_lesson_ids)
        pct = int((completed_in_cat / total_lessons * 100)) if total_lessons else 0
        skills.append({
            'category': cat.name,
            'icon': cat.icon,
            'color': cat.color,
            'percentage': min(pct, 100),
        })

    streak, _ = LearningStreak.objects.get_or_create(user=user)

    return Response({
        'total_points': user.total_points,
        'streak': LearningStreakSerializer(streak).data,
        'progress_by_type': by_type,
        'skills': skills,
        'certificates': CertificateSerializer(
            Certificate.objects.filter(user=user), many=True
        ).data,
        'enrollments': EnrollmentSerializer(
            Enrollment.objects.filter(user=user).select_related('course'), many=True
        ).data,
    })
