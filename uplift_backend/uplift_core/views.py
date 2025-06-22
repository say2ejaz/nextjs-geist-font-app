from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import MoodEntry, JournalEntry, ContentModule, CommunityGroup, CommunityPost, DirectMessage, CrisisContact
from .serializers import (
    UserSerializer, MoodEntrySerializer, JournalEntrySerializer, ContentModuleSerializer,
    CommunityGroupSerializer, CommunityPostSerializer, DirectMessageSerializer, CrisisContactSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .ai_module import analyze_sentiment, detect_harmful_content

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('pseudonymous_username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(pseudonymous_username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username, password=password)
        serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class MoodEntryViewSet(viewsets.ModelViewSet):
    queryset = MoodEntry.objects.all()
    serializer_class = MoodEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        note = serializer.validated_data.get('note', '')
        sentiment_score = analyze_sentiment(note)
        serializer.save(user=self.request.user)
        # Additional logic can be added to store sentiment_score if needed

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content', '')
        sentiment_score = analyze_sentiment(content)
        serializer.save(user=self.request.user)
        # Additional logic can be added to store sentiment_score if needed

class ContentModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentModule.objects.all()
    serializer_class = ContentModuleSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def feed(self, request):
        # For MVP, return all content; later filter by mood_affinity and user mood
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

class CommunityGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommunityGroup.objects.all()
    serializer_class = CommunityGroupSerializer
    permission_classes = [IsAuthenticated]

class CommunityPostViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(group__in=self.request.user.communitygroup_set.all(), moderation_status='approved')

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content', '')
        if detect_harmful_content(content):
            moderation_status = 'pending'
        else:
            moderation_status = 'approved'
        serializer.save(user=self.request.user, moderation_status=moderation_status)

class DirectMessageViewSet(viewsets.ModelViewSet):
    queryset = DirectMessage.objects.all()
    serializer_class = DirectMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user) | self.queryset.filter(receiver=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # For MVP, just acknowledge report receipt
        content_id = request.data.get('content_id')
        content_type = request.data.get('content_type')
        reason = request.data.get('reason')
        # Logic to flag content for review would go here
        return Response({'status': 'Report received'}, status=status.HTTP_200_OK)

class CrisisContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CrisisContact.objects.all()
    serializer_class = CrisisContactSerializer
    permission_classes = [permissions.AllowAny]
