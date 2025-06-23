from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html

from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User
from decimal import Decimal

class Car(models.Model):
    CATEGORY_CHOICES = [
        ('SUV', 'SUV'),
        ('Truck', 'Truck'),
        ('Electric', 'Electric'),
        ('Sedan', 'Sedan'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, default='Unknown')
    model = models.CharField(max_length=100, default='Unknown')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.IntegerField(default=0.00)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/cars_img/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.brand} {self.model})"

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="auto" />', self.image.url)
        return "No Image"

    image_tag.short_description = 'Image Preview'




   

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

 
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            days = (self.end_date - self.rental_date).days or 1
            price_per_day = Decimal(str(self.car.price))
            self.total_price = price_per_day * Decimal(days)
        except (InvalidOperation, TypeError, ValueError) as e:
            print(f"Error calculating total_price: {e}")
            self.total_price = Decimal('0.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.car} from {self.rental_date} to {self.end_date}"