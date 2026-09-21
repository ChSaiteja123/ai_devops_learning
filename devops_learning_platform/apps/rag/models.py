from django.db import models
from django.conf import settings


class Document(models.Model):
    """Uploaded document for the RAG knowledge base."""
    SOURCE_CHOICES = [
        ('upload', 'File Upload'), ('url', 'URL'), ('manual', 'Manual Entry'),
    ]
    CATEGORY_CHOICES = [
        ('devops', 'DevOps'), ('aws', 'AWS'), ('kubernetes', 'Kubernetes'),
        ('terraform', 'Terraform'), ('monitoring', 'Monitoring'),
        ('ai', 'AI Engineering'), ('runbook', 'Runbook'), ('architecture', 'Architecture'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('processing', 'Processing'),
        ('indexed', 'Indexed'), ('failed', 'Failed'),
    ]

    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='upload')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='devops')
    file = models.FileField(upload_to='rag_docs/', blank=True, null=True)
    url = models.URLField(blank=True)
    content = models.TextField(blank=True, help_text='Raw extracted text')
    chunk_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    indexed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.category}] {self.title}'


class RAGQuery(models.Model):
    """Log of all RAG queries for analysis."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    query = models.TextField()
    answer = models.TextField()
    source_documents = models.JSONField(default=list)
    confidence_score = models.FloatField(default=0.0)
    response_time_ms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'RAG Query'
        verbose_name_plural = 'RAG Queries'

    def __str__(self):
        return self.query[:80]
