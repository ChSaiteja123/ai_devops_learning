from django.db import models
from apps.courses.models import Course


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_limit_minutes = models.PositiveIntegerField(default=20)
    passing_score = models.PositiveIntegerField(default=70, help_text='Percentage required to pass')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course.title} — {self.title}'


class Question(models.Model):
    TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('truefalse', 'True / False'),
        ('scenario', 'Scenario Based'),
        ('troubleshoot', 'Troubleshooting'),
        ('architecture', 'Architecture Design'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='mcq')
    explanation = models.TextField(help_text='Shown after the user answers')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:80]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{"✅" if self.is_correct else "❌"} {self.text[:60]}'


class QuizAttempt(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    passed = models.BooleanField(default=False)
    responses = models.JSONField(default=dict, help_text='{question_id: answer_id}')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    weak_areas = models.JSONField(default=list)

    def __str__(self):
        return f'{self.user.username} — {self.quiz.title} — {self.score}%'
