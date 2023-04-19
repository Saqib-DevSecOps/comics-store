import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView

from src.administration.admins.models import (
    Product, ProductVersion, Version, ProductImage, Post, PostCategory, Category, Order, Language,
)
from src.website.filters import ProductFilter, PostFilter
from src.website.utility import session_id

""" BASIC PAGES ---------------------------------------------------------------------------------------------- """


class HomeTemplateView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['new_products'] = Product.objects.order_by('-created_on')[:10]
        context['most_like'] = Product.objects.order_by('-likes')[:10]
        context['most_sale'] = Product.objects.order_by('-sales')[:10]
        return context


class ContactUsTemplateView(TemplateView):
    template_name = 'website/contact_us.html'


class AboutUsTemplateView(TemplateView):
    template_name = 'website/about.html'


""" COMICS AND NOVELS PAGES ------------------------------------------------------------------------------------ """


class ProductListView(ListView):
    template_name = 'website/product_list.html'
    queryset = Product.objects.all()
    paginate_by = 24

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category and self.request is not None:
            product = Product.objects.prefetch_related('category').filter(categories__name=category)
        else:
            product = Product.objects.all().order_by('-created_at')
        filter_product = ProductFilter(self.request.GET, queryset=product)
        pagination = Paginator(filter_product.qs, 10)
        page_number = self.request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        context['products'] = page_obj
        context['filter_form'] = filter_product
        return context


class ProductDetailView(DetailView):
    template_name = 'website/product_detail.html'
    model = Product
    pk_url_kwarg = "product_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context


""" ---------------- POST PAGES ------------------------------------------------------------------------------------ """


class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'website/post_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        category = self.request.GET.get('category')
        print(category)

        if category and self.request is not None:
            post = Post.objects.filter(category__id=category)
        else:
            post = Post.objects.all().order_by('-created_on')
        context['recent'] = Post.objects.order_by('-created_on')[:5]
        context['popular_posts'] = Post.objects.order_by('-visits', '-read_time')[:5]
        filter_posts = PostFilter(self.request.GET, queryset=post)
        pagination = Paginator(filter_posts.qs, 10)
        page_number = self.request.GET.get('page')
        print(page_number)
        page_obj = pagination.get_page(page_number)
        context['post_category'] = PostCategory.objects.all()
        context['posts'] = page_obj
        context['filter_form'] = filter_posts
        context['category'] = category
        return context


class PostDetailView(DetailView):
    template_name = 'website/post_detail.html'
    model = Post
    pk_url_kwarg = "post_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        return context


""" ORDER AND CART  ------------------------------------------------------------------------------------------ """

import json


def add_to_cart(request, product_id, version):
    # Retrieve the cart data from the cookie
    cart_json = request.COOKIES.get('cart', '{}')
    cart_json = cart_json.replace("'", "\"")
    cart = json.loads(cart_json)
    print(cart)
    print(cart.keys())
    print(type(cart))
    product_id  = str(product_id + product_id + int(version))
    # Add the product to the cart
    if product_id in cart:
        print('inside cart')
        # Check if the same version of the product is already in the cart
        if cart[product_id]['version'] == version:
            print('inside more')
            cart[product_id]['quantity'] += 1
        else:
            # Add new product version to the cart
            print('inside else')
            product = {
                'id': product_id,
                'name': 'Product name',
                'version': version,
                'quantity': 1,
                # Add any other relevant product information
            }
            cart[product_id] = product
    else:
        # Add new product to the cart
        print('else')
        product = {
            'id': product_id,
            'name': 'Product name',
            'version': version,
            'quantity': 1,
            # Add any other relevant product information
        }
        cart[product_id] = product

    # Set the cart data as a cookie
    response = redirect('website:home')
    response.set_cookie('cart', json.dumps(cart))

    return response


class RemoveFromCartView(View):
    pass


@method_decorator(login_required, name='dispatch')
class OrderDetail(DetailView):
    pass


""" ISSUES PAGES ---------------------------------------------------------------------------------------------- """


class CartTemplateView(TemplateView):
    template_name = 'website/cart.html'
