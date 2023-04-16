from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView

from src.administration.admins.models import (
    Product, ProductVersion, Version, ProductImage, Post, PostCategory, Category, Order, Cart, Language
)
from src.website.filters import ProductFilter

""" BASIC PAGES ---------------------------------------------------------------------------------------------- """


class HomeTemplateView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['new_products'] = Product.objects.order_by('-created_on')[:10]
        context['most_like'] = Product.objects.order_by('-likes')[:10]
        context['most_saled'] = Product.objects.order_by('-sales')[:10]
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


class PostListView(ListView):
    template_name = 'website/post_list.html'
    queryset = Post.objects.all()
    paginate_by = 24

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
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


@method_decorator(login_required, name='dispatch')
class OrderDetail(DetailView):
    pass


@method_decorator(login_required, name='dispatch')
class AddToCartView(CreateView):
    pass


@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(DeleteView):
    pass


@method_decorator(login_required, name='dispatch')
class UpdateCartQuantityView(UpdateView):
    pass


""" ISSUES PAGES ---------------------------------------------------------------------------------------------- """


class ComicsTemplateView(TemplateView):
    template_name = 'website/comic.html'


class NovelTemplateView(TemplateView):
    template_name = 'website/novel.html'


class BlogTemplateView(TemplateView):
    template_name = 'website/blog.html'


class BlogDetailTemplateView(TemplateView):
    template_name = 'website/about_us_detail.html'


class CartTemplateView(TemplateView):
    template_name = 'website/cart.html'
