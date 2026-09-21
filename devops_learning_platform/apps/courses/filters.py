import django_filters
from .models import Course


class CourseFilter(django_filters.FilterSet):
    difficulty = django_filters.ChoiceFilter(choices=Course.DIFFICULTY_CHOICES)
    platform_level = django_filters.ChoiceFilter(choices=Course.LEVEL_CHOICES)
    category = django_filters.CharFilter(field_name='category__slug')
    is_featured = django_filters.BooleanFilter()

    class Meta:
        model = Course
        fields = ['difficulty', 'platform_level', 'category', 'is_featured']
