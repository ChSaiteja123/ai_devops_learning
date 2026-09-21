from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'topic', 'message_count', 'messages', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()


class ConversationListSerializer(serializers.ModelSerializer):
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'topic', 'message_count', 'last_message', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        msg = obj.messages.last()
        return msg.content[:100] if msg else None


class ChatInputSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=4000)
    conversation_id = serializers.IntegerField(required=False, allow_null=True)
    topic = serializers.CharField(max_length=100, required=False, allow_blank=True)
