from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from tinymce.models import HTMLField

from src.accounts.models import User

""" INVENTORY """


class Language(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Version(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    BOOK_TYPE_CHOICE = (
        ('comic', 'Comic'),
        ('novel', 'Novel'),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    thumbnail_image = models.ImageField(upload_to='books/images/thumbnails', null=True, blank=True)

    artist = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    translator = models.CharField(max_length=255)
    illustrator = models.CharField(max_length=255)

    book_type = models.CharField(max_length=15, default='novel', choices=BOOK_TYPE_CHOICE)
    categories = models.ManyToManyField(Category)
    languages = models.ManyToManyField(Language)

    pages = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    sales = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.thumbnail_image.delete(save=True)
        super(Product, self).delete(*args, **kwargs)

    def get_images(self):
        return ProductImage.objects.filter(product=self)

    def get_versions(self):
        return ProductVersion.objects.filter(product=self)


class ProductVersion(models.Model):
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=255)
    price = models.FloatField(default=0)

    class Meta:
        ordering = ''

    def __str__(self):
        return f"{self.product.name} {self.version.name}"


class ProductImage(models.Model):
    image = models.ImageField(upload_to='books/images/product_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        ordering = ['product']
        verbose_name_plural = "Product Images"

    def __str__(self):
        return self.product.name

    def delete(self, *args, **kwargs):
        self.image.delete(save=True)
        super(ProductImage, self).delete(*args, **kwargs)


""" ORDERS """


class Order(models.Model):

    PAYMENT_STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    ORDER_STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('shipping', 'Shipping'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    total = models.FloatField(default=0)
    paid = models.FloatField(default=0)

    stripe_payment_id = models.CharField(max_length=1000)
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICE, default='pending')
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICE, default='pending')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user.name_or_username()} ordered."


class Cart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order} {self.product.name}."


""" BLOG DETAILS """


class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Post Categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS = (
        ('draft', "Draft"),
        ('publish', "Publish")
    )

    image = models.ImageField(upload_to='books/images/posts', null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = HTMLField()

    read_time = models.PositiveIntegerField(default=0, help_text='read time in minutes')
    visits = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=15, choices=STATUS, default='publish')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
