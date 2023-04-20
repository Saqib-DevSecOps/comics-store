from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_resized import ResizedImageField

"""
At the start please be careful to start migrations
--------------------------------------------------

STEP: 1 comment current_subscription [FIELD] in model [USER]
STEP: 1 py manage.py makemigrations accounts
STEP: 2 py manage.py migrate
Then do next ...

"""


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=200)
    profile_image = ResizedImageField(
        upload_to='accounts/images/profiles/', null=True, blank=True, size=[250, 250], quality=75, force_format='PNG',
        help_text='size of logo must be 250*250 and format must be png image file', crop=['middle', 'center']
    )
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    is_client = models.BooleanField(default=True)

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def name_or_username(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="user_registered")
def on_user_registration(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=200)
    Province = models.CharField(max_length=250)
    City = models.CharField(max_length=250)
    street_address_1 = models.CharField(max_length=250)
    street_address_2 = models.CharField(max_length=250,null=True,blank=True)
    postal_code = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email