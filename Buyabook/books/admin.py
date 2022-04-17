from django.contrib import admin

from Buyabook.books.models import Category, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def books_count(self, obj):
        return Book.objects.all().filter(category_id=obj.pk)
    list_display = ('name', 'books_count')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'seller', 'is_available',)


