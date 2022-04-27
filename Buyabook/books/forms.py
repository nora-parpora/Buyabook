from django import forms
from django.shortcuts import get_object_or_404

from Buyabook.accounts.helpers import BootstrapFormMixin
from Buyabook.accounts.models import Profile
from Buyabook.books.models import Book


class AddBookForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        book = super().save(commit=False)

        profile = get_object_or_404(Profile, pk=self.user.id)
        book.seller = profile

        if commit:
            book.save()

        return book

    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'category', 'pages', 'price', 'image')

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 1,
                }
            ),
        }


class UpdateBookForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
    """ Additional Library: /
    django-cleanup==6.0.0 which is added to the INSTALLED_APPS/
    is handling the deletion from the DB """

    class Meta:
        model = Book
        exclude = ('seller', 'cart',)  # ToDo
        # Show widget value for image to display current picture {{ widget.value.url }}

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 1
                }),
            'image': forms.FileInput()

        }


class RetrieveBookForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    class Meta:
        model = Book
        exclude = ('seller', 'cart',)
