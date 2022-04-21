from django.db import models
from PIL import Image
from Buyabook.accounts.models import Profile
from Buyabook.books.validators import validate_add_to_cart_perm
from Buyabook.cart.models import Cart


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
    image = models.ImageField(upload_to='images/',
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


    def save(self, **kwargs):
        super().save()

        # if validate_add_to_cart_perm(self):
        #     pass
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:

                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


    def __str__(self):
        return f'{self.title}'


