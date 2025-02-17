from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    FAVORITE_TYPES = (
        ('FLIGHT', 'Flight'),
        ('HOTEL', 'Hotel'),
        ('COUNTRY', 'Country')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=FAVORITE_TYPES)
    item_data = models.JSONField()  # Store the details of favorited item
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'type', 'item_data']

    def __str__(self):
        return f"{self.user.username}'s {self.type} favorite"