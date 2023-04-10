from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class HomeTemplateView(TemplateView):
    template_name = 'website/home.html'


class ShopTemplateView(TemplateView):
    template_name = 'website/store.html'
