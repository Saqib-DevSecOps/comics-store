from django.urls import path

from src.website.views import HomeTemplateView, \
    ContactUsTemplateView, PostListView, CartTemplateView, AboutUsTemplateView, \
    ProductListView, ProductDetailView, PostDetailView, AddToCart, IncrementCart, DecrementCart, \
    RemoveFromCartView, OrderCreate, SuccessPayment, CancelPayment, ReadSample, CookiePolicy, PrivacyPolicy, \
    TermsAndCondition, Jobs

app_name = "website"
urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('shop/', ProductListView.as_view(), name='shop'),
    path('product-detail/<str:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('post-detail/<str:slug>', PostDetailView.as_view(), name='post-detail'),

    path('about-us/', AboutUsTemplateView.as_view(), name='about_us'),
    path('contact-us/', ContactUsTemplateView.as_view(), name='contact_us'),

    path('cart/', CartTemplateView.as_view(), name='cart'),
    path('add_to_cart/', AddToCart.as_view(), name='add-to-cart'),
    path('remove-cart/', RemoveFromCartView.as_view(), name='remove-cart'),
    path('increment/cart/item', IncrementCart.as_view(), name='increment'),
    path('decrement/cart/item', DecrementCart.as_view(), name='decrement'),

    path('billing', OrderCreate.as_view(), name='order'),
    path('payment-success/', SuccessPayment.as_view(), name="success"),
    path('payment-cancelled/', CancelPayment.as_view(), name="cancel"),

    path('read/sample/<str:pk>', ReadSample.as_view(), name="read_sample"),

    path('cookie-policy/', CookiePolicy.as_view(), name='cookie'),
    path('privacy-policy/', PrivacyPolicy.as_view(), name='privacy'),
    path('terms-and-conditions/', TermsAndCondition.as_view(), name='terms'),
    path('jobs/', Jobs.as_view(), name='jobs')
]
