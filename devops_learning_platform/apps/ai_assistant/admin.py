from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['role', 'content', 'tokens_used', 'created_at']
    can_delete = False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'topic', 'message_count', 'updated_at']
    list_filter = ['topic', 'created_at']
    search_fields = ['user__username', 'title']
    inlines = [MessageInline]

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = '💬 Messages'
