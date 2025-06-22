from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pseudonymous_username = models.CharField(max_length=150, unique=True)
    creation_timestamp = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'pseudonymous_username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.pseudonymous_username

class MoodEntry(models.Model):
    MOOD_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 scale

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    timestamp = models.DateTimeField(default=timezone.now)
    mood_score = models.IntegerField(choices=MOOD_CHOICES)
    note = models.TextField(blank=True)  # For MVP, plain text; encryption to be added later

    def __str__(self):
        return f"{self.user} - Mood {self.mood_score} at {self.timestamp}"

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField(blank=True)  # For MVP, plain text; encryption to be added later

    def __str__(self):
        return f"{self.user} - Journal at {self.timestamp}"

class ContentModule(models.Model):
    TYPE_CHOICES = [
        ('article', 'Article'),
        ('meditation', 'Meditation'),
        ('affirmation', 'Affirmation'),
    ]
    MOOD_AFFINITY_CHOICES = [
        ('low', 'Low'),
        ('stressed', 'Stressed'),
        ('neutral', 'Neutral'),
    ]

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    content = models.TextField()
    tags = models.CharField(max_length=255, blank=True)  # comma-separated
    mood_affinity = models.CharField(max_length=20, choices=MOOD_AFFINITY_CHOICES)

    def __str__(self):
        return self.title

class CommunityGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CommunityPost(models.Model):
    MODERATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    group = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    moderation_status = models.CharField(max_length=20, choices=MODERATION_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Post by {self.user} in {self.group} at {self.timestamp}"

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return f"DM from {self.sender} to {self.receiver} at {self.timestamp}"

class CrisisContact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    website_url = models.URLField(blank=True)

    def __str__(self):
        return self.name
