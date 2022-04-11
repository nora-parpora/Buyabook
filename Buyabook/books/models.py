from django.db import models
from PIL import Image
from Buyabook.accounts.models import Profile


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
    owner = models.ForeignKey(Profile,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    image = models.ImageField(upload_to='images/',
                              null=True,
                              blank=True,)


    pages = models.PositiveIntegerField(
        blank=True,
        null=True,)

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:

            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    def __str__(self):
        return f'{self.title}'


