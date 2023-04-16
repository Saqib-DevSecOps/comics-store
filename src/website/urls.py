from django.urls import path

from src.website.views import HomeTemplateView, \
    ContactUsTemplateView, PostListView, CartTemplateView, AboutUsTemplateView, \
    ProductListView, PostDetailView

app_name = "website"
urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('shop/', ProductListView.as_view(), name='shop'),

    path('stories/', PostListView.as_view(), name='posts'),
    path('story-detail/<str:slug>', PostDetailView.as_view(), name='post-detail'),

    path('about-us/', AboutUsTemplateView.as_view(), name='about_us'),
    path('contact-us/', ContactUsTemplateView.as_view(), name='contact_us'),

    path('cart/', CartTemplateView.as_view(), name='cart'),

]
