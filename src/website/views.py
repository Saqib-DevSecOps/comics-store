from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class HomeTemplateView(TemplateView):
    template_name = 'website/home.html'


class ComicsTemplateView(TemplateView):
    template_name = 'website/comic.html'


class NovelTemplateView(TemplateView):
    template_name = 'website/novel.html'


class BlogTemplateView(TemplateView):
    template_name = 'website/blog.html'


class AboutUsTemplateView(TemplateView):
    template_name = 'website/about.html'


class BlogDetailTemplateView(TemplateView):
    template_name = 'website/about_us_detail.html'


class ContactUsTemplateView(TemplateView):
    template_name = 'website/contact_us.html'


class CartTemplateView(TemplateView):
    template_name = 'website/cart.html'
