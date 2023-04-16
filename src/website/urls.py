from django.urls import path

from src.website.views import HomeTemplateView, ComicsTemplateView, NovelTemplateView, \
    BlogDetailTemplateView, ContactUsTemplateView, BlogTemplateView, CartTemplateView, AboutUsTemplateView, \
    ProductListView

app_name = "website"
urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('shop/', ProductListView.as_view(), name='shop'),
    path('novels/', NovelTemplateView.as_view(), name='novel'),

    path('stories/', BlogTemplateView.as_view(), name='stories'),
    path('story-detail/', BlogDetailTemplateView.as_view(), name='stories-detail'),

    path('about-us/', AboutUsTemplateView.as_view(), name='about_us'),
    path('contact-us/', ContactUsTemplateView.as_view(), name='contact_us'),

    path('cart/', CartTemplateView.as_view(), name='cart'),

]
