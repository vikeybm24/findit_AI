from django.db import models

# Create your models here.
# File path: api/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# This is the corrected code
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # Add these two lines to fix the clashing error
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set', # Unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set', # Unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self):
        return self.email

class LostItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    date_lost = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='lost_items_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='searching')

    def __str__(self):
        return f"{self.item_name} lost by {self.user.email}"

class FoundItem(models.Model):
    finder = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    date_found = models.DateField()
    location_found = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='found_items_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='available')

    def __str__(self):
        return f"{self.item_name} found by {self.finder.email}"