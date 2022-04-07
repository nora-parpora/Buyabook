from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.forms import ModelForm

from Buyabook.accounts.helpers import BootstrapFormMixin, DisabledFieldsFormMixin
from Buyabook.accounts.models import Profile


class CreateProfileForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
        widget=forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            )
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter last name',
            }
        )
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter email',
            }
        )
    )
    city = forms.CharField(
        max_length=Profile.CITY_MAX_LENGTH,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your city here',
            }
        )
    )
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter your address here',
                'rows': 2,
            }
        )
    )

    phone = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Enter your phone here',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            city = self.cleaned_data['city'],
            address=self.cleaned_data['address'],
            phone=self.cleaned_data['phone'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Enter a username',
                }
            ),
        }


class UpdateProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'email', 'city', 'address')

        widgets = {
            'address': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
        }


class DeleteProfileForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        #  TO_DO: Delete all associated books
        self.instance.delete()
        return self.instance

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'email', 'city', 'address')