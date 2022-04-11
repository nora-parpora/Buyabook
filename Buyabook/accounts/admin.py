from django.contrib import admin

from Buyabook.accounts.models import Profile, BaBUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(BaBUser)
class BaBAdmin(admin.ModelAdmin):
    list_display = ('username', 'id')

