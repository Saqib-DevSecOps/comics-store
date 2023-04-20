from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, UpdateView, ListView

from src.accounts.models import Address
from src.administration.admins.models import Wishlist, Order
from src.administration.client.forms import AddressForm, UserProfileForm


# Create your views here.
@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='client/user_update_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='client/user_update_form.html', context=context)


@method_decorator(login_required, name='dispatch')
class AddressUpdate(View):

    def get(self, request):
        form = AddressForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='client/address_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your address updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='client/address_form.html', context=context)


@method_decorator(login_required, name='dispatch')
class ClientDashboard(TemplateView):
    template_name = 'client/client_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(ClientDashboard, self).get_context_data(**kwargs)
        context['total_orders'] = Order.objects.filter(user=self.request.user).count()
        context['pending_orders'] = Order.objects.filter(user=self.request.user, order_status="pending").count()
        context['wishlist'] = Wishlist.objects.filter(user=self.request.user).count()
        return context


@method_decorator(login_required, name='dispatch')
class WishlistView(ListView):
    model = Wishlist
    template_name = 'client/wishlist_list.html'
    context_object_name = 'objects'


@method_decorator(login_required, name='dispatch')
class WishListDelete(View):
    def get(self, request, pk, *args, **kwargs):
        wishlist = get_object_or_404(Wishlist, product_id=pk, user=self.request.user)
        wishlist.delete()
        messages.success(request, 'Wishlist Item Deleted Success Fully')
        return redirect("client:wishlist")
