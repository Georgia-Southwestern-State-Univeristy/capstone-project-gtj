from django.contrib import admin
from .models import CurrencyRate

@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('base_currency', 'target_currency', 'rate', 'last_updated')
    list_filter = ('base_currency', 'target_currency')
    search_fields = ('base_currency', 'target_currency')
    ordering = ('base_currency', 'target_currency')