from django.contrib import admin
from .models import ChatHistory
# Register your models here.

class ChateHistoryAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'message', 'response', 'last_response', 'created_at']
    
admin.site.register(ChatHistory, ChateHistoryAdmin)
