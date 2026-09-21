from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizAttempt


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']  # Never expose is_correct in list


class AnswerWithCorrectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'order', 'answers']


class QuestionWithExplanationSerializer(serializers.ModelSerializer):
    answers = AnswerWithCorrectSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'order', 'answers', 'explanation']


class QuizListSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'description', 'time_limit_minutes', 'passing_score', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.count()


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'description', 'time_limit_minutes', 'passing_score', 'questions']


class QuizSubmitSerializer(serializers.Serializer):
    """Input for submitting a quiz: {question_id: answer_id}"""
    responses = serializers.DictField(child=serializers.IntegerField())


class QuizAttemptResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'score', 'passed', 'responses', 'started_at', 'completed_at', 'weak_areas']
