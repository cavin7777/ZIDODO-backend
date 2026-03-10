from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProgress

from django.contrib.auth import get_user_model

from .models import Location, Quest, UserQuest, Reward, UserReward
from .serializers import (
    UserProgressSerializer,
    UserSerializer,
    RegisterSerializer,
    LocationSerializer,
    QuestSerializer,
    RewardSerializer
)

User = get_user_model()


# ==========================
# HOME VIEW
# ==========================
def home(request):
    return HttpResponse("Hello from myapp")


# ==========================
# REGISTER VIEW
# ==========================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# ==========================
# LIST ALL USERS
# ==========================
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# ==========================
# RETRIEVE USER BY ID
# ==========================
class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


# ==========================
# PROFILE VIEW
# ==========================
class ProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# =====================================================
# LOCATION VIEWS
# =====================================================

class LocationListCreateView(generics.ListCreateAPIView):
    """
    GET /locations/  → anyone can view
    POST /locations/ → only admins can create
    """
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


# =====================================================
# QUEST VIEWS
# =====================================================

class QuestListView(generics.ListAPIView):
    queryset = Quest.objects.filter(is_active=True)
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]


class QuestDetailView(generics.RetrieveAPIView):
    queryset = Quest.objects.filter(is_active=True)
    serializer_class = QuestSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


class CompleteQuestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        quest = get_object_or_404(Quest, id=id)

        # Check if quest already completed
        if UserQuest.objects.filter(user=user, quest=quest).exists():
            return Response(
                {"error": "Quest already completed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create completion record
        UserQuest.objects.create(user=user, quest=quest)

        # Add quest points to user
        user.points += quest.points
        user.save()

        # Update or create progress
        progress, created = UserProgress.objects.get_or_create(user=user)

        progress.quests_completed += 1
        progress.total_points = user.points
        progress.save()

        return Response(
            {
                "message": "Quest completed successfully",
                "points_earned": quest.points,
                "total_points": user.points
            },
            status=status.HTTP_200_OK
        )


# =====================================================
# REWARD VIEWS
# =====================================================

class RewardListView(generics.ListAPIView):
    queryset = Reward.objects.filter(is_active=True)
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]


class RedeemRewardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        reward = get_object_or_404(Reward, id=id)

        # Check if user has enough points
        if user.points < reward.points_required:
            return Response(
                {"error": "Not enough points"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deduct points from user
        user.points -= reward.points_required
        user.save()

        # Create reward redemption record
        UserReward.objects.create(user=user, reward=reward)

        # Update user progress
        progress, created = UserProgress.objects.get_or_create(user=user)

        progress.rewards_redeemed += 1
        progress.total_points = user.points
        progress.save()

        return Response(
            {
                "message": "Reward redeemed successfully",
                "points_spent": reward.points_required,
                "remaining_points": user.points
            },
            status=status.HTTP_200_OK
        )
    

# =====================================================
# PROGRESS VIEWS
# =====================================================

class UserProgressView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        progress = UserProgress.objects.get(user=request.user)

        serializer = UserProgressSerializer(progress)

        return Response(serializer.data)