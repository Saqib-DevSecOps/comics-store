from django.urls import path
from .views import (
    UserPasswordResetView, UserListView, UserUpdateView, UserDeleteView, UserDetailView, UserCreateView
)

app_name = 'admins'

urlpatterns = [
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/add/', UserCreateView.as_view(), name='user-add'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('user/<int:pk>/reset/password/', UserPasswordResetView.as_view(), name='user-password-reset'),
]

