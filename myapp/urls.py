from django.urls import path
from .views import (
    LocationListCreateView,
    home,
    RegisterView,
    ProfileView,
    UserListCreateView,
    UserRetrieveView,
    QuestListView,
    QuestDetailView,
    CompleteQuestView,
    RewardListView,
    RedeemRewardView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # ==========================
    # HOME
    # ==========================
    path('', home, name='home'),

    # ==========================
    # AUTHENTICATION
    # ==========================
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    # ==========================
    # USER
    # ==========================
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/', UserListCreateView.as_view(), name='users'),
    path('users/<uuid:id>/', UserRetrieveView.as_view(), name='user-detail'),

    # ==========================
    # LOCATIONS
    # ==========================
    path('locations/', LocationListCreateView.as_view(), name='locations'),

    # ==========================
    # QUESTS
    # ==========================
    path('quests/', QuestListView.as_view(), name='quests'),
    path('quests/<uuid:id>/', QuestDetailView.as_view(), name='quest-detail'),
    path('quests/<uuid:id>/complete/', CompleteQuestView.as_view(), name='complete-quest'),

    # ==========================
    # REWARDS
    # ==========================
    path('rewards/', RewardListView.as_view(), name='rewards'),
    path('rewards/<uuid:id>/redeem/', RedeemRewardView.as_view(), name='redeem-reward'),
]