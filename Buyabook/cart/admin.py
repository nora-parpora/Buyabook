from django.contrib import admin
from django.contrib.admin import StackedInline

from Buyabook.books.models import Book
from Buyabook.cart.models import Cart


class BookInlineAdmin(admin.StackedInline):
    model = Book


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def books_count(self, obj):
        return Book.objects.all().filter(cart_id=obj.pk)
    list_display = ('user', 'books_count')
    inlines = (BookInlineAdmin, )

