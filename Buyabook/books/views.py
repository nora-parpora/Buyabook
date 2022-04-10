from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from Buyabook.accounts.models import Profile
from Buyabook.books.forms import AddBookForm


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

