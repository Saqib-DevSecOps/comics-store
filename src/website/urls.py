from django.urls import path

from src.website.views import HomeTemplateView,ShopTemplateView

app_name = "website"
urlpatterns = [
    path('',HomeTemplateView.as_view(),name='home'),
    path('store/',ShopTemplateView.as_view(),name='store')
]
