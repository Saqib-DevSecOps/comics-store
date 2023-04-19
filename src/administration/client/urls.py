from django.urls import path

from src.administration.client.views import ClientDashboard

app_name = 'client'
urlpatterns = [
    path('', ClientDashboard.as_view(), name='dashboard')
]
