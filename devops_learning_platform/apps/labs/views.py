from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lab, LabSubmission
from .serializers import LabListSerializer, LabDetailSerializer, LabSubmissionSerializer


class LabViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Lab.objects.filter(is_published=True)
        tech = self.request.query_params.get('technology')
        if tech:
            qs = qs.filter(technology=tech)
        return qs

    def get_serializer_class(self):
        return LabDetailSerializer if self.action == 'retrieve' else LabListSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def submit(self, request, pk=None):
        """POST /api/v1/labs/{id}/submit/ — mark lab as completed"""
        lab = self.get_object()
        submission, created = LabSubmission.objects.get_or_create(
            lab=lab, user=request.user,
            defaults={
                'notes': request.data.get('notes', ''),
                'time_taken_minutes': request.data.get('time_taken_minutes', 0),
            }
        )
        if created:
            from apps.progress.models import UserProgress
            UserProgress.objects.get_or_create(
                user=request.user, content_type='lab', object_id=lab.id,
                defaults={'completed': True, 'points_earned': 25}
            )
        return Response(LabSubmissionSerializer(submission).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
