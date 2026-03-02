from django.urls import path
from . import views
from .views import UserListCreateView, UserRetrieveView

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', UserListCreateView.as_view(), name='users'),
    path('users/<uuid:id>/', UserRetrieveView.as_view(), name='user-detail'),
]