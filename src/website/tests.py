from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from src.administration.admins.models import Product, Category, Language


class ProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create categories
        cls.category_1 = Category.objects.create(name='Category 1')
        cls.category_2 = Category.objects.create(name='Category 2')
        # Create languages
        cls.language_1 = Language.objects.create(name='Language 1')
        cls.language_2 = Language.objects.create(name='Language 2')
        # Create products
        cls.product_1 = Product.objects.create(
            name='Product 1',
            slug='product-1',
            description='Description 1',
            artist='Artist 1',
            author='Author 1',
            translator='Translator 1',
            illustrator='Illustrator 1',
            pages=100,
            clicks=10,
            sales=5,
            likes=20,
            is_active=True,
            created_on=timezone.now(),
        )
        cls.product_1.categories.set([cls.category_1, cls.category_2])
        cls.product_1.languages.set([cls.language_1, cls.language_2])
        cls.product_2 = Product.objects.create(
            name='Product 2',
            slug='product-2',
            description='Description 2',
            artist='Artist 2',
            author='Author 2',
            translator='Translator 2',
            illustrator='Illustrator 2',
            pages=200,
            clicks=20,
            sales=10,
            likes=30,
            is_active=True,
            created_on=timezone.now(),
        )
        cls.product_2.categories.set([cls.category_2])
        cls.product_2.languages.set([cls.language_2])
        cls.url = reverse('website:product_list')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'website/product_list.html')

    def test_view_pagination_is_twenty_four(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context_data['product_list']), 2)

    def test_view_lists_all_products(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context_data['product_list']), Product.objects.count())

    def test_view_lists_filtered_products_by_category(self):
        url = f"{self.url}?category={self.category_1}"
        response = self.client.get(url)
        self.assertEqual(len(response.context_data['product_list']), self.category_1.product_set.count())

    def test_view_lists_filtered_products_by_language(self):
        url = f"{self.url}?language={self.language_1}"
        response = self.client.get(url)
        self.assertEqual(len(response.context_data['product_list']), self.language_1.product_set.count())
