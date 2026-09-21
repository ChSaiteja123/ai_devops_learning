from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Course
from .serializers import CategorySerializer, CourseListSerializer, CourseDetailSerializer
from .filters import CourseFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_published=True).select_related('category')
    permission_classes = [permissions.AllowAny]
    filterset_class = CourseFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category__name']
    ordering_fields = ['created_at', 'title', 'estimated_duration_hours']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """GET /api/v1/courses/featured/ — list featured courses"""
        qs = self.get_queryset().filter(is_featured=True)
        serializer = CourseListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_level(self, request):
        """GET /api/v1/courses/by_level/?level=level1"""
        level = request.query_params.get('level')
        qs = self.get_queryset()
        if level:
            qs = qs.filter(platform_level=level)
        serializer = CourseListSerializer(qs, many=True)
        return Response(serializer.data)
