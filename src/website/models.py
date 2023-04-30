from django.db import models


# Create your models here.


class HomeSliderImage(models.Model):
    image = models.ImageField(upload_to='background/images/')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"website image  {str(self.id)}"


class Banner(models.Model):
    image = models.ImageField(upload_to='background/images/')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"website image  {str(self.id)}"
