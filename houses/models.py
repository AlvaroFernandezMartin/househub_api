from django.db import models
from django.conf import settings 

class House(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    image = models.ImageField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    description = models.TextField()
    street = models.CharField(max_length=255)
    house_number = models.PositiveIntegerField()
    house_number_addition = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    construction_year = models.PositiveIntegerField()
    has_garage = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
