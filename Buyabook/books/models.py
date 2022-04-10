from django.db import models

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
                              blank=True,
                              default='images/book.png')

    pages = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title}'
