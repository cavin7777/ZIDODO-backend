from django.urls import path
from .views import home, RegisterView, ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', home),

    # Register
    path('register/', RegisterView.as_view(), name='register'),

    # Login (JWT)
    path('login/', TokenObtainPairView.as_view(), name='login'),

    # Refresh Token
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    # Protected route
    path('profile/', ProfileView.as_view(), name='profile'),
]