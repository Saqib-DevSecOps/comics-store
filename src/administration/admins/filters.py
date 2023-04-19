import django_filters
from django.forms import TextInput

from src.accounts.models import User
from src.administration.admins.models import Product


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'username'}), lookup_expr='icontains')
    email = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'email'}), lookup_expr='icontains')

    class Meta:
        model = User
        fields = {'is_active', 'is_client'}


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Name'}), lookup_expr='icontains')
    artist = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Artist'}), lookup_expr='icontains')
    author = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Author'}), lookup_expr='icontains')

    class Meta:
        model = Product
        fields = {'book_type'}

