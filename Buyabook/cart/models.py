from django.db import models

from Buyabook.accounts.models import BaBUser


class Cart(models.Model):
    user = models.OneToOneField(BaBUser,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                )
    def __str__(self):
        return f'{self.user}'

