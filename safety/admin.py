from django.contrib import admin
from .models import CountrySafety

@admin.register(CountrySafety)
class CountrySafetyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'region', 'overall_safety_score', 'women_safety_score')
    search_fields = ('name', 'code')
    list_filter = ('region',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'capital', 'region')
        }),
        ('Safety Scores', {
            'fields': ('overall_safety_score', 'women_safety_score', 'night_safety_score', 
                      'crime_score')
        }),
        ('Safety Information', {
            'fields': ('safety_summary', 'women_safety_info', 'night_safety_info',
                      'solo_traveler_info', 'crime_info', 'transportation_safety_info', 
                      'emergency_numbers')
        }),
    )