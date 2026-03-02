from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, RegisterSerializer

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
    """
    Endpoint for registering a new user.
    """
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
    """
    Returns the currently logged-in user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)