from rest_framework import serializers
from .models import User, MoodEntry, JournalEntry, ContentModule, CommunityGroup, CommunityPost, DirectMessage, CrisisContact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'pseudonymous_username', 'creation_timestamp']

class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = ['id', 'user', 'timestamp', 'mood_score', 'note']

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'user', 'timestamp', 'content']

class ContentModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentModule
        fields = ['id', 'title', 'type', 'content', 'tags', 'mood_affinity']

class CommunityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityGroup
        fields = ['id', 'name', 'description']

class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = ['id', 'user', 'group', 'timestamp', 'content', 'moderation_status']

class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'receiver', 'timestamp', 'content']

class CrisisContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisContact
        fields = ['id', 'name', 'phone_number', 'website_url']
