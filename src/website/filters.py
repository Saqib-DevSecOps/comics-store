import django_filters
from django.db.models import Q
from django.forms import TextInput

from src.administration.admins.models import Product


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label=''
                                      , widget=TextInput(attrs={'placeholder': 'Search Here',
                                                                'class': 'form-control rounded-pill'}),
                                      method='blog_filter')

    class Meta:
        model = Product
        fields = ['title', ]

    def product_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


