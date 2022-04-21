
from django.db.models import Q
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from Buyabook.accounts.helpers import CurrentUserView

from Buyabook.books.forms import AddBookForm, UpdateBookForm
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
    # model = Book
    template_name = 'catalogue.html'
    #  queryset = Book.objects.all()
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

        # query = self.request.GET.get("q")
        # if query:
        #     object_list = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query)).order_by("title")
        #     # object_list = Book.objects.filter(
        #     #     Q(pk=query) )
        # else:
        #     object_list = Book.objects.all()
        # return object_list


class BookDetailsView(DetailView, CurrentUserView):
    model = Book
    template_name = 'book_details.html'


class UpdateBookView(UpdateView,CurrentUserView):
    """  Additional Library: django-cleanup==6.0.0 which is added to the INSTALLED_APPS/
    is handling the deletion from the DB """
    model = Book
    form_class = UpdateBookForm
    template_name = 'update_book.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().is_available():
            return redirect('404')
        return super().dispatch(request, *args, **kwargs)


class DeleteBookView(DeleteView,CurrentUserView):
    model = Book
    #  form_class = DeleteProfileForm
    template_name = 'delete_book.html'
    success_url = reverse_lazy('index')

    # def get_object(self, queryset=None):
    #     instance = get_bab_obj(Book, pk=self.request.book.pk)
    #     return instance

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['book'] = get_bab_obj(Book, pk=self.request.user.id)
    #     return context


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
