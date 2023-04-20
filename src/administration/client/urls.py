from django.urls import path

from src.administration.client.views import ClientDashboard, WishlistView, WishListDelete, UserUpdateView, AddressUpdate

app_name = 'client'
urlpatterns = [
    path('', ClientDashboard.as_view(), name='dashboard'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/delete/<str:pk>', WishListDelete.as_view(), name='wishlist-delete'),
    path('user/change/', UserUpdateView.as_view(), name='user-change'),
    path('user/address/update/', AddressUpdate.as_view(), name='user-address-update'),
]
