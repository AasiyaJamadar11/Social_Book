# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    public_visibility = models.BooleanField(default=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    @property
    def age(self):
        if self.birth_year:
            return date.today().year - self.birth_year
        return None

    def __str__(self):
        return self.username

    

class UploadedFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True)
    description = models.TextField(blank=True)
    visibility = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    year_published = models.IntegerField(null=False, default=2020)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



