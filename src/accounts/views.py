from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View, UpdateView
from django.contrib.auth import logout
from src.accounts.forms import UserProfileForm, AddressForm
from src.accounts.models import Address


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('account_login')


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):

    def get(self, request):
        if request.user.is_superuser:
            return redirect("/admin/")
        elif request.user.is_staff:
            return redirect('admins:dashboard')
        else:
            return redirect('client:dashboard')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)


@method_decorator(login_required, name='dispatch')
class AddressUpdate(View):

    def get(self, request):
        form = AddressForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/address_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your address updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/address_form.html', context=context)





