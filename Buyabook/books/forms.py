from django import forms
from django.shortcuts import get_object_or_404

from Buyabook.accounts.helpers import BootstrapFormMixin
from Buyabook.accounts.models import Profile
from Buyabook.books.models import Book


class AddBookForm(forms.ModelForm,BootstrapFormMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        book = super().save(commit=False)

        profile = get_object_or_404(Profile, pk=self.user.id)
        book.owner = profile


        if commit:
            book.save()

        return book

    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'category', 'pages',)

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 1,
                }
            ),
        }

