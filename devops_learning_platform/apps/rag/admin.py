from django.contrib import admin
from .models import Document, RAGQuery


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'source_type', 'status', 'chunk_count', 'created_at']
    list_filter = ['category', 'status', 'source_type']
    search_fields = ['title']
    readonly_fields = ['chunk_count', 'status', 'error_message', 'indexed_at']
    actions = ['reindex_documents']

    def reindex_documents(self, request, queryset):
        from .services import RAGService
        service = RAGService()
        for doc in queryset:
            service.index_document(doc)
        self.message_user(request, f'Reindexed {queryset.count()} documents.')
    reindex_documents.short_description = '🔄 Re-index selected documents'


@admin.register(RAGQuery)
class RAGQueryAdmin(admin.ModelAdmin):
    list_display = ['query_short', 'user', 'confidence_score', 'response_time_ms', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['user', 'query', 'answer', 'source_documents', 'confidence_score', 'response_time_ms', 'created_at']

    def query_short(self, obj):
        return obj.query[:80]
    query_short.short_description = 'Query'
