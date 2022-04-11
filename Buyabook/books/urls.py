from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from Buyabook.accounts.views import logged_in_switch_view, DashboardView, HomeView
from Buyabook.books.views import AddBookView, CatalogueView

urlpatterns = [
    #path('', RedirectView.as_view(url=reverse_lazy('dashboard')), name='home'),
    path('add-book/', AddBookView.as_view(), name = 'add book'),
    path('', logged_in_switch_view(DashboardView.as_view(), HomeView.as_view()), name='index'),
    path('catalogue', CatalogueView.as_view(), name='catalogue'),

]