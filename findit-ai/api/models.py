import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField
import random

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True)

    def __str__(self):
        return self.email

class LostItem(models.Model):
    STATUS_CHOICES = [('searching', 'Searching'), ('reunited', 'Reunited')]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    date_lost = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='lost_items_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='searching')
    embeddings = JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} lost by {self.user.email}"

class FoundItem(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('claimed', 'Claim in Progress'), ('reunited', 'Reunited')]
    finder = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    date_found = models.DateField()
    location_found = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='found_items_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    embeddings = JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} found by {self.finder.email}"


def generate_word_token():
    adjectives = ["blue", "bright", "calm", "fast", "golden", "happy", "silent", "smart", "swift", "tiny", "green", "sunny", "wild"]
    nouns = ["river", "mountain", "leaf", "cloud", "stone", "bird", "star", "tree", "flame", "sky", "dream", "path", "wind"]
    return f"{random.choice(adjectives)}-{random.choice(nouns)}"

class Claim(models.Model):
    METHOD_CHOICES = [('manual', 'Manual Claim'), ('ai_suggestion', 'AI Suggestion')]
    STATUS_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('resolved', 'Resolved'), ('match_found', 'Match Found')]
    
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, related_name='claims')
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='claims', null=True, blank=True)
    claimant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    chat_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    creation_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='manual')
    
    # --- THIS FIELD IS UPDATED ---
    # We remove 'default' and make it nullable to handle the save logic correctly.
    exchange_token = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return f"Claim by {self.claimant.email} on {self.found_item.item_name}"

    # --- THIS SAVE METHOD IS ADDED ---
    # This logic now runs every time a new Claim is saved
    def save(self, *args, **kwargs):
        if not self.exchange_token:
            # Generate a new unique token if one doesn't exist
            self.exchange_token = generate_word_token()
            # Ensure it's unique by checking the database
            while Claim.objects.filter(exchange_token=self.exchange_token).exists():
                self.exchange_token = generate_word_token()
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE, unique=True)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Testimonial for Claim ID {self.claim.id} by {self.user.username}'

class ChatMessage(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']
    def __str__(self):
        return f'Message by {self.sender.username} in Claim {self.claim.id} at {self.timestamp}'