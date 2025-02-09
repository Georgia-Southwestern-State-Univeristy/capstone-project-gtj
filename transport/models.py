from django.db import models
from django.contrib.auth.models import User

class Airport(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)
    
class Ride(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE) 
    pickup_time = models.DateTimeField()
    dropoff_location = models.CharField(max_length=200)