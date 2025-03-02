# safety/models.py
from django.db import models

class CountrySafety(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)  # Change this to 3 since some codes are 3 chars
    capital = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    
    # Safety scores - all as integers
    overall_safety_score = models.IntegerField(default=0)
    women_safety_score = models.IntegerField(default=0)
    night_safety_score = models.IntegerField(default=0)
    crime_score = models.IntegerField(default=0)
    
    # Safety information
    safety_summary = models.TextField(blank=True)
    women_safety_info = models.TextField(blank=True)
    night_safety_info = models.TextField(blank=True)
    solo_traveler_info = models.TextField(blank=True)  
    crime_info = models.TextField(blank=True)
    transportation_safety_info = models.TextField(blank=True)
    emergency_numbers = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Countries'