from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, ListView

from src.accounts.models import Address


# Create your views here.

@method_decorator(login_required, name='dispatch')
class ClientDashboard(TemplateView):
    template_name = 'client/client_dashboard.html'


class WishlistView(ListView):
    pass
