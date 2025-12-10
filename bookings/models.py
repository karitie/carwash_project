from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Booking(models.Model):
    SERVICE_CHOICES = [
        ('Basic Wash', 'Basic Wash'),
        ('Full Wash', 'Full Wash'),
        ('Interior Cleaning', 'Interior Cleaning'),
        ('Engine Wash', 'Engine Wash'),
    ]
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    car_type = models.CharField(max_length=50)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service}"
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    

