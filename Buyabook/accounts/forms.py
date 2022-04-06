from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.forms import ModelForm

from Buyabook.accounts.helpers import BootstrapFormMixin
from Buyabook.accounts.models import Profile

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('first_name', 'last_name', 'email')
#         widgets = {
#             'first_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter first name',
#                 }
#             ),
#             'last_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter last name',
#                 }
#             ),
#             'email': forms.EmailInput(
#                 attrs={
#
#                     'placeholder': 'Enter Email',
#                 }
#             ),
#         }


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
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
            'password1': forms.PasswordInput(
                attrs={
                    'placeholder': 'Choose password',
                }
            ),
            # 'password2': forms.TextInput(
            #     attrs={
            #         'placeholder': 'Repeat password',
            #     }
            # ),
            # 'email': forms.EmailInput(
            #     attrs={
            #
            #         'placeholder': 'Enter Email',
            #     }
            # ),
        }
