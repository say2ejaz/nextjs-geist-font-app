from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, MoodEntryViewSet, JournalEntryViewSet, ContentModuleViewSet,
    CommunityGroupViewSet, CommunityPostViewSet, DirectMessageViewSet,
    ReportView, CrisisContactViewSet
)

router = DefaultRouter()
router.register(r'moods', MoodEntryViewSet, basename='mood')
router.register(r'journals', JournalEntryViewSet, basename='journal')
router.register(r'content', ContentModuleViewSet, basename='content')
router.register(r'community/groups', CommunityGroupViewSet, basename='communitygroup')
router.register(r'community/posts', CommunityPostViewSet, basename='communitypost')
router.register(r'messages', DirectMessageViewSet, basename='directmessage')
router.register(r'crisis_contacts', CrisisContactViewSet, basename='crisiscontact')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('reports/', ReportView.as_view(), name='reports'),
    path('', include(router.urls)),
]
