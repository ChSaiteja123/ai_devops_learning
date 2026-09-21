from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ['text', 'is_correct']


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'time_limit_minutes', 'passing_score', 'is_published']
    list_filter = ['is_published', 'course__category']
    search_fields = ['title', 'course__title']
    list_editable = ['is_published']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'question_type', 'order']
    list_filter = ['question_type', 'quiz__course__category']
    search_fields = ['text']
    inlines = [AnswerInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'passed', 'started_at']
    list_filter = ['passed', 'started_at']
    readonly_fields = ['user', 'quiz', 'score', 'passed', 'responses', 'started_at', 'completed_at', 'weak_areas']
