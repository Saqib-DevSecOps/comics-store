from django.urls import path, include
from .views import LogoutView, CrossAuthView, UserUpdateView, AddressUpdate

app_name = 'accounts'
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/change/', UserUpdateView.as_view(), name='user-change'),
    path('user/address/update/', AddressUpdate.as_view(), name='user-address-update'),
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth')
]


