from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from Buyabook.accounts.models import Profile
from Buyabook.books.forms import AddBookForm
from Buyabook.books.models import Book


class AddBookView(CreateView):
    template_name = 'add_book.html'
    form_class = AddBookForm
    success_url = reverse_lazy('index')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['owner'] = get_object_or_404(Profile, pk=self.request.user.id)
    #     return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CatalogueView(ListView):

    template_name = 'catalogue.html'
    # queryset = Book.objects.all()
    context_object_name = 'books'

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        if query:
            object_list = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query))
            #object_list = Book.objects.filter(Q(category__exact=query))
        else:
            object_list = Book.objects.all()
        return object_list

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['owner'] = get_object_or_404(Profile, pk=self.request.user.id)
    #     return context





