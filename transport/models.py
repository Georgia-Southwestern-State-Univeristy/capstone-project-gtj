from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    transit_website = models.URLField(help_text="Official transit authority website")
    
    def __str__(self):
        return f"{self.name}, {self.country}"
    
    class Meta:
        verbose_name_plural = "cities"

class TransitPass(models.Model):
    PASS_TYPES = [
        ('DAY', 'Day Pass'),
        ('WEEK', 'Weekly Pass'),
        ('MONTH', 'Monthly Pass'),
        ('SINGLE', 'Single Ride'),
    ]
    
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='transit_passes')
    name = models.CharField(max_length=100)
    pass_type = models.CharField(max_length=10, choices=PASS_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)  # e.g., USD, GBP, EUR
    purchase_url = models.URLField(help_text="Where to buy this pass")
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.city.name}"

class TransitLine(models.Model):
    LINE_TYPES = [
        ('METRO', 'Metro/Subway'),
        ('BUS', 'Bus'),
        ('TRAM', 'Tram'),
        ('TRAIN', 'Train'),
        ('FERRY', 'Ferry'),
        ('BIKE', 'Bike Share'),
    ]
    
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='transit_lines')
    name = models.CharField(max_length=100)
    line_type = models.CharField(max_length=10, choices=LINE_TYPES)
    description = models.TextField()
    schedule_url = models.URLField(help_text="Link to line schedule")
    map_url = models.URLField(help_text="Link to line map")
    operating_hours = models.CharField(max_length=200)
    frequency = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.get_line_type_display()}) - {self.city.name}"

class TransitStation(models.Model):
    line = models.ForeignKey(TransitLine, on_delete=models.CASCADE, related_name='stations')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    accessibility = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.line.name}"