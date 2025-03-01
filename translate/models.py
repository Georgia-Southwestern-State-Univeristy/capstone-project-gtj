from django.db import models
from django.contrib.auth.models import User

class TranslationRequest(models.Model):
    """
    Model to store translation requests (optional, for tracking/analytics)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    source_text = models.TextField()
    translated_text = models.TextField()
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.source_language} to {self.target_language} - {self.created_at}"