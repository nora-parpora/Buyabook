from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView

from Buyabook.accounts.helpers import get_bab_obj, CurrentUserView
from Buyabook.accounts.models import Profile
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
            object_list = Book.objects.filter(qs)
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


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'book'

    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, pk=self.request.user.id)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    #    profile = get_object_or_404(Profile, pk=self.request.user.id)
    #     context.update({
    #         'is_owner': self.object.user_id == self.request.user.id,
    #     })
        return context


class UpdateBookView(UpdateView): #  Additional Library: django-cleanup==6.0.0 which is added to the INSTALLED_APPS/
    # is handling the deletion from the DB
    model = Book
    form_class = UpdateBookForm
    template_name = 'update_book.html'
    success_url = reverse_lazy('index')


