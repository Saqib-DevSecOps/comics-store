import base64

import PyPDF2
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, UpdateView, ListView, DetailView
from fitz import fitz
from pdf2image import convert_from_bytes, convert_from_path

from src.accounts.models import Address
from src.administration.admins.models import Wishlist, Order, Product, OrderItem
from src.administration.client.forms import AddressForm, UserProfileForm

import io
from PyPDF2 import PdfFileReader
from PIL import Image
from django.shortcuts import get_object_or_404, render


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
class WishCreateView(View):
    def get(self, request, pk):
        wishlist = Wishlist.objects.filter(user=self.request.user, product_id=pk)
        wish = wishlist.exists()
        product = Product.objects.get(id=pk)
        if wish:
            messages.success(request, 'Already in Wish List')
            print('hello')
            return redirect('website:product-detail', product.slug)
        wishlist = Wishlist.objects.create(user=self.request.user, product_id=pk)
        messages.success(request, 'Added to wishlist')
        return redirect('website:product-detail', product.slug)


@method_decorator(login_required, name='dispatch')
class WishlistView(ListView):
    model = Wishlist
    template_name = 'client/wishlist_list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class WishListDelete(View):
    def get(self, request, pk, *args, **kwargs):
        wishlist = get_object_or_404(Wishlist, product_id=pk, user=self.request.user)
        wishlist.delete()
        messages.success(request, 'Wishlist Item Deleted Success Fully')
        return redirect("client:wishlist")


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = OrderItem
    template_name = 'client/order_list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return self.model.objects.filter(order__user=self.request.user).exclude(Q(order__order_status='completed')
                                                                                | Q(order__order_status='cancelled')
                                                                                )


@method_decorator(login_required, name='dispatch')
class AddressList(ListView):
    model = Order
    template_name = 'client/address.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class BooksListView(ListView):
    model = OrderItem
    template_name = 'client/books.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return self.model.objects.filter(order__user=self.request.user)


def download_file(request, pk):
    # Assuming that the file is stored in a media folder called "files"
    product = get_object_or_404(Product, id=pk)
    print(product)
    print(product.book_file)
    file_path = f'media/{product.book_file}'
    print(file_path)
    # Open the file in binary mode using the built-in open() function
    with open(file_path, 'rb') as file:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{product.book_file}"'
            return response


@method_decorator(login_required, name='dispatch')
class ReadBook(View):
    def get(self, request, pk, *args, **kwargs):
        pdf_file = Product.objects.get(id=pk)
        images = convert_from_path(pdf_file.book_file.path)

        image_data = []
        for image in images:
            with io.BytesIO() as output:
                image.save(output, format='PNG')
                image_data.append(base64.b64encode(output.getvalue()).decode('utf-8'))

        context = {'images': image_data}
        return render(request, 'client/sample_book.html', context)
