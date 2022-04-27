from django.db import models
from Buyabook.accounts.models import Profile
from Buyabook.cart.models import Cart
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        )

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(
        max_length=100,
        )
    author = models.CharField(
        max_length=100,
        )
    description = models.TextField(
        blank=True,
        null=True
        )
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    price = models.FloatField()
    seller = models.ForeignKey(Profile,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    image = CloudinaryField('image',
                            null=True,
                            blank=True,
                            )
    cart = models.ForeignKey(Cart,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             )

    pages = models.PositiveIntegerField(
        blank=True,
        null=True,)

    def is_available(self):
        return self.cart == None

    def __str__(self):
        return f'{self.title}'


