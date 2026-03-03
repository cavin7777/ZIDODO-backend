from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from .models import Location, Quest, UserQuest, Reward, UserReward
from .serializers import (
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
# LIST ALL USERS (Optional)
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
# PROFILE VIEW (Protected)
# ==========================
class ProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# =====================================================
# LOCATION VIEWS
# =====================================================

class LocationListView(generics.ListAPIView):
    """
    GET /locations/
    Returns all active locations.
    """
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


# =====================================================
# QUEST VIEWS
# =====================================================

class QuestListView(generics.ListAPIView):
    """
    GET /quests/
    Returns all active quests.
    """
    queryset = Quest.objects.filter(is_active=True)
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]


class QuestDetailView(generics.RetrieveAPIView):
    """
    GET /quests/<id>/
    Returns single quest with questions.
    """
    queryset = Quest.objects.filter(is_active=True)
    serializer_class = QuestSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


# ==========================
# COMPLETE QUEST VIEW
# ==========================
class CompleteQuestView(APIView):
    """
    POST /quests/<id>/complete/
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        user = request.user
        quest = get_object_or_404(Quest, id=id)

        # Check if already completed
        if UserQuest.objects.filter(user=user, quest=quest).exists():
            return Response(
                {"error": "Quest already completed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create completion record
        UserQuest.objects.create(user=user, quest=quest)

        # Add points to user
        user.points += quest.points
        user.save()

        return Response(
            {"message": "Quest completed successfully"},
            status=status.HTTP_200_OK
        )


# =====================================================
# REWARD VIEWS
# =====================================================

class RewardListView(generics.ListAPIView):
    """
    GET /rewards/
    Returns all active rewards.
    """
    queryset = Reward.objects.filter(is_active=True)
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]


class RedeemRewardView(APIView):
    """
    POST /rewards/<id>/redeem/
    """

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

        # Deduct points
        user.points -= reward.points_required
        user.save()

        # Create reward record
        UserReward.objects.create(user=user, reward=reward)

        return Response(
            {"message": "Reward redeemed successfully"},
            status=status.HTTP_200_OK
        )