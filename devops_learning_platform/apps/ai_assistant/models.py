from django.db import models
from django.conf import settings


class Conversation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations',
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200, blank=True)
    topic = models.CharField(max_length=100, blank=True, help_text='e.g. Docker, Kubernetes, AWS')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.username}: {self.title or "Untitled"}'


class Message(models.Model):
    ROLE_CHOICES = [('user', 'User'), ('assistant', 'Assistant')]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    tokens_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[{self.role}] {self.content[:60]}'
