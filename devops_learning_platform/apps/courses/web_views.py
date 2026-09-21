from django.shortcuts import get_object_or_404, render

from .models import Course
from apps.lessons.models import Lesson
from .lesson_extensions import LESSON_EXTENSIONS
from .lesson_page_data import COMMAND_EXPANSIONS, SECTION_LABELS, SECTION_ORDER
from .platform_deep_dive_content import PLATFORM_COMMANDS, PLATFORM_EXTENSIONS


def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('lessons'),
        slug=slug,
        is_published=True,
    )
    lessons = list(course.lessons.filter(is_published=True))
    return render(request, 'courses/detail.html', {'course': course, 'lessons': lessons})


def lesson_detail(request, slug, order):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lesson = get_object_or_404(Lesson, course=course, order=order, is_published=True)
    lessons = list(course.lessons.filter(is_published=True))
    current_index = lessons.index(lesson)
    previous_lesson = lessons[current_index - 1] if current_index > 0 else None
    next_lesson = lessons[current_index + 1] if current_index + 1 < len(lessons) else None
    return render(request, 'lessons/detail.html', {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'lesson_number': current_index + 1,
        'extension': ({**LESSON_EXTENSIONS, **PLATFORM_EXTENSIONS}).get(current_index + 1, {}),
    })


def lesson_section(request, slug, order, section):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lesson = get_object_or_404(Lesson, course=course, order=order, is_published=True)
    if section not in SECTION_ORDER:
        from django.http import Http404
        raise Http404('Unknown lesson section')
    lessons = list(course.lessons.filter(is_published=True))
    extension = ({**LESSON_EXTENSIONS, **PLATFORM_EXTENSIONS}).get(order, {})
    return render(request, 'lessons/section.html', {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
        'lesson_number': order,
        'section': section,
        'section_label': SECTION_LABELS[section],
        'section_order': SECTION_ORDER,
        'section_labels': SECTION_LABELS,
        'section_navigation': [{'slug': item, 'label': SECTION_LABELS[item]} for item in SECTION_ORDER],
        'extension': extension,
        'expanded_commands': ({**COMMAND_EXPANSIONS, **PLATFORM_COMMANDS}).get(order, []),
    })
