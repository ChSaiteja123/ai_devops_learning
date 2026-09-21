from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Quiz, Question, Answer, QuizAttempt
from .serializers import (
    QuizListSerializer, QuizDetailSerializer, QuizSubmitSerializer,
    QuizAttemptResultSerializer, QuestionWithExplanationSerializer
)


class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.filter(is_published=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return QuizDetailSerializer if self.action == 'retrieve' else QuizListSerializer

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        POST /api/v1/quizzes/{id}/submit/
        Body: {"responses": {"1": 3, "2": 7, ...}}  (question_id: answer_id)

        Returns: score, passed, correct answers, explanations, weak areas
        """
        quiz = self.get_object()
        serializer = QuizSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        responses = serializer.validated_data['responses']
        questions = quiz.questions.prefetch_related('answers').all()

        correct_count = 0
        total = questions.count()
        weak_areas = []
        detailed_results = []

        for question in questions:
            qid = str(question.id)
            selected_id = responses.get(qid)
            correct_answer = question.answers.filter(is_correct=True).first()
            is_correct = selected_id and int(selected_id) == (correct_answer.id if correct_answer else None)

            if is_correct:
                correct_count += 1
            else:
                weak_areas.append(question.text[:100])

            detailed_results.append({
                'question_id': question.id,
                'question': question.text,
                'selected_answer_id': selected_id,
                'correct_answer_id': correct_answer.id if correct_answer else None,
                'is_correct': is_correct,
                'explanation': question.explanation,
            })

        score = round((correct_count / total) * 100, 2) if total > 0 else 0
        passed = score >= quiz.passing_score

        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            passed=passed,
            responses={str(k): v for k, v in responses.items()},
            completed_at=timezone.now(),
            weak_areas=weak_areas[:5],
        )

        if passed:
            from apps.progress.models import UserProgress
            UserProgress.objects.get_or_create(
                user=request.user, content_type='quiz', object_id=quiz.id,
                defaults={'completed': True, 'points_earned': 30}
            )

        return Response({
            'attempt_id': attempt.id,
            'score': score,
            'passed': passed,
            'correct': correct_count,
            'total': total,
            'passing_score': quiz.passing_score,
            'weak_areas': weak_areas[:5],
            'detailed_results': detailed_results,
            'message': '🎉 Congratulations! You passed!' if passed else f'Keep practicing! You need {quiz.passing_score}% to pass.',
        })

    @action(detail=False, methods=['get'])
    def my_attempts(self, request):
        attempts = QuizAttempt.objects.filter(user=request.user).order_by('-started_at')
        return Response(QuizAttemptResultSerializer(attempts, many=True).data)
