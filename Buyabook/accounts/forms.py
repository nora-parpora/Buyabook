from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model


from Buyabook.accounts.helpers import BootstrapFormMixin
from Buyabook.accounts.models import Profile
from Buyabook.books.models import Book
from Buyabook.cart.models import Cart


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
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your city here',
            }
        )
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter your address here',
                'rows': 2,
            }
        )
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '+359XXXXXXXXX',
            })
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
            city=self.cleaned_data['city'],
            address=self.cleaned_data['address'],
            phone=self.cleaned_data['phone'],
            user=user,
        )
        cart = Cart(user=user)

        if commit:
            profile.save()
            cart.save()
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'email', 'city', 'address')

        widgets = {
            'address': forms.Textarea(
                attrs={
                    'rows': 1,
                }),
        }


class DeleteProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        Book.objects.filter(seller=self.instance).delete()
        self.instance.delete()
        return self.instance


class BaBPasswordChangeForm(forms.Form):
    error_messages = {
        "password_mismatch": "The two password fields didn’t match.",
    }

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=None,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    class Meta:
        model = get_user_model()
