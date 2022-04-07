from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator

from Buyabook.accounts.managers import BaBUserManager
from Buyabook.accounts.validators import validate_only_letters


class BaBUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_MAX_LENGTH = 25

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = BaBUserManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 3
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 3
    LAST_NAME_MAX_LENGTH = 30
    CITY_MAX_LENGTH = 30

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    email = models.EmailField(
        unique=True,
        help_text='Please, provide a valid email address',
    )

    phone = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=CITY_MAX_LENGTH,
        null=True,
        blank=True
    )
    address = models.TextField(
        null=True,
        blank=True
    )

    user = models.OneToOneField(
        BaBUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

"""
ToDo:
Phone number
Address - ? whether to apply a model or a prop
Address - 121

"""