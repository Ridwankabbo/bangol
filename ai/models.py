from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_message')
    message = models.TextField()
    response = models.TextField()
    last_response = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['created_at']
    
