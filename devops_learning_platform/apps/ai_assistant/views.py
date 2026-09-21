from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, ConversationListSerializer, ChatInputSerializer, MessageSerializer
)
from .services import AIAssistantService


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return ConversationSerializer if self.action == 'retrieve' else ConversationListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def chat(request):
    """
    POST /api/v1/ai/chat/

    Body:
    {
        "message": "Explain Kubernetes pods",
        "conversation_id": 5,   // optional — omit to start new conversation
        "topic": "Kubernetes"   // optional
    }

    Returns: {"conversation_id": 5, "reply": "..."}
    """
    serializer = ChatInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user if request.user.is_authenticated else None
    conv_id = serializer.validated_data.get('conversation_id')
    topic = serializer.validated_data.get('topic', '')
    message = serializer.validated_data['message']

    if conv_id:
        try:
            conversation = Conversation.objects.get(id=conv_id, user=user) if user else None
            if conversation is None:
                return Response({'error': 'Conversation not found or anonymous access is not allowed for this chat.'}, status=status.HTTP_404_NOT_FOUND)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        if user:
            conversation = Conversation.objects.create(user=user, topic=topic)
        else:
            conversation = Conversation.objects.create(topic=topic)

    service = AIAssistantService()
    reply = service.chat(conversation, message)

    return Response({
        'conversation_id': conversation.id,
        'reply': reply,
        'topic': conversation.topic,
    })
