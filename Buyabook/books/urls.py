from django.urls import path, include

from Buyabook.books.views import AddBookView

urlpatterns = [
    path('add-book/', AddBookView.as_view(), name = 'add book'),

]