from django.contrib import admin
from .models import TranslationRequest

@admin.register(TranslationRequest)
class TranslationRequestAdmin(admin.ModelAdmin):
    list_display = ('source_language', 'target_language', 'created_at', 'user')
    list_filter = ('source_language', 'target_language', 'created_at')
    search_fields = ('source_text', 'translated_text')
    readonly_fields = ('source_text', 'translated_text', 'source_language', 'target_language', 'created_at')
    
    def has_add_permission(self, request):
        return False