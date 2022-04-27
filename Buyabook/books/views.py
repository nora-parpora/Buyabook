from django.db.models import Q
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from Buyabook.accounts.helpers import CurrentUserView

from Buyabook.books.forms import AddBookForm, UpdateBookForm, RetrieveBookForm
from Buyabook.books.models import Book


class AddBookView(CreateView):
    template_name = 'add_book.html'
    form_class = AddBookForm
    success_url = reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CatalogueView(ListView, CurrentUserView):
    template_name = 'catalogue.html'
    context_object_name = 'books'

    def get_queryset(self):
        object_list = None
        query = self.request.GET.get('q')
        if query:
            qs = Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query)

            if query.isdigit():
                qs |= Q(pk=query)
            object_list = Book.objects.filter(qs).order_by("title")
            if len(object_list) == 0:
                return
        else:
            object_list = Book.objects.all()
        return object_list



class BookDetailsView(DetailView, CurrentUserView):
    model = Book
    template_name = 'book_details.html'


class UpdateBookView(UpdateView, CurrentUserView):
    """  Additional Library: django-cleanup==6.0.0 which is added to the INSTALLED_APPS/
    is handling the deletion from the DB """
    model = Book
    form_class = UpdateBookForm
    template_name = 'update_book.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().is_available():
            return render(request, 'restricted_for_editing.html', {'book': self.get_object()})
        return super().dispatch(request, *args, **kwargs)


class RetrieveBookView(TemplateView, CurrentUserView):
    model = Book
    template_name = 'retrieve_success.html'


class DeleteBookView(DeleteView, CurrentUserView):
    model = Book
    template_name = 'delete_book.html'
    success_url = reverse_lazy('index')


class RestrictedForEditView(TemplateView):
    template_name = 'restricted_for_editing.html'


class AvailableBooksView(ListView):
    model = Book
    template_name = 'available_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        object_list = None
        query = self.request.GET.get('q')

        if query:
            qs = Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query)
            if query.isdigit():
                qs |= Q(pk=query)
        else:
            qs = Q(cart_id=None) & ~Q(seller_id=self.request.user.id)

        object_list = Book.objects.filter(qs).order_by("title")
        if len(object_list) == 0:
            return
        return object_list
