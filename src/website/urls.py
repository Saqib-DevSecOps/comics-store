from django.urls import path

from src.website.views import HomeTemplateView, \
    ContactUsTemplateView, PostListView, CartTemplateView, AboutUsTemplateView, \
    ProductListView, ProductDetailView, PostDetailView, AddToCart, IncrementCart, DecrementCart, \
    RemoveFromCartView, OrderCreate

app_name = "website"
urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('shop/', ProductListView.as_view(), name='shop'),
    path('product-detail/<str:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('stories/', PostListView.as_view(), name='posts'),
    path('story-detail/<str:slug>', PostDetailView.as_view(), name='post-detail'),

    path('about-us/', AboutUsTemplateView.as_view(), name='about_us'),
    path('contact-us/', ContactUsTemplateView.as_view(), name='contact_us'),

    path('cart/', CartTemplateView.as_view(), name='cart'),
    path('add_to_cart/', AddToCart.as_view(), name='add-to-cart'),
    path('remove-cart/', RemoveFromCartView.as_view(), name='remove-cart'),
    path('increment/cart/item', IncrementCart.as_view(), name='increment'),
    path('decrement/cart/item', DecrementCart.as_view(), name='decrement'),

    path('billing', OrderCreate.as_view(), name='order')
]
