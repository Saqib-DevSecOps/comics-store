from django import forms

from .models import (
    Product, ProductVersion, Version, ProductImage, Post
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'thumbnail_image', 'name',
            'book_type', 'categories', 'languages', 'pages',
            'artist', 'author', 'translator', 'illustrator',
            'description', 'is_active'
        ]


class ProductVersionForm(forms.ModelForm):
    class Meta:
        model = ProductVersion
        fields = [
            'version', 'isbn', 'price'
        ]


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [
            'image', 'description'
        ]
