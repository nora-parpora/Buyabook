from django.urls import path

from Buyabook.accounts.views import logged_in_switch_view, DashboardView, HomeView
from Buyabook.books.views import AddBookView, CatalogueView, BookDetailsView, UpdateBookView, DeleteBookView, \
    AvailableBooksView, RetrieveBookView

urlpatterns = [

    path('add-book/', AddBookView.as_view(), name='add book'),
    path('update-book/<int:pk>/', UpdateBookView.as_view(), name='update book'),
    path('retrieve-book/', RetrieveBookView.as_view(), name='retrieve book'),
    path('delete-book/<int:pk>/', DeleteBookView.as_view(), name='delete book'),
    path('book-details/<int:pk>/', BookDetailsView.as_view(), name='book details'),
    path('', logged_in_switch_view(DashboardView.as_view(), HomeView.as_view()), name='index'),
    path('catalogue/', CatalogueView.as_view(), name='catalogue'),
    path('buyabook/', AvailableBooksView.as_view(), name='buyabook'),

]
