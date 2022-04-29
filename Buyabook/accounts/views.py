from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, DeleteView, ListView

from Buyabook.accounts.forms import CreateProfileForm, UpdateProfileForm, BaBPasswordChangeForm
from Buyabook.accounts.helpers import AuthCheckView, CurrentUserView, get_bab_obj
from Buyabook.accounts.models import Profile, BaBUser
from Buyabook.books.models import Book


class UserRegisterView(CreateView):
    form_class = CreateProfileForm
    template_name = 'create_profile.html'
    success_url = reverse_lazy('login')


class HomeView(ListView):  # Showing the landing page when the user is not logged in.
    template_name = 'catalogue.html'
    queryset = Book.objects.all()
    context_object_name = 'books'


class DashboardView(LoginRequiredMixin, ListView, CurrentUserView, AuthCheckView):
    queryset = Book.objects.all()
    template_name = 'catalogue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(seller_id=self.request.user.id)
        context['all_books'] = Book.objects.all()
        return context


class UserLoginView(auth_views.LoginView):
    template_name = 'login_page.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return get_bab_obj(Profile, pk=self.request.user.id)


class ChangeUserPasswordView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'change_password.html'
    form_class = BaBPasswordChangeForm
    success_url = reverse_lazy('update profile')

    def get_object(self, queryset=None):
        return get_bab_obj(Profile, pk=self.request.user.id)


class ProfileDetailsView(LoginRequiredMixin, DetailView, UserLoginView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile = get_bab_obj(Profile, pk=self.request.user.id)
        return profile


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = BaBUser
    template_name = 'delete_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        instance = get_bab_obj(BaBUser, pk=self.request.user.id)
        return instance


class RequestDeleteView(DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """
    success_message = "Deleted Successfully"

    def get_queryset(self):
        qs = super(RequestDeleteView, self).get_queryset()
        return qs.filter(seller=self.request.user)


class UnauthView(TemplateView):
    template_name = '401.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def logged_in_switch_view(logged_in_view, logged_out_view):
    def inner_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return logged_in_view(request, *args, **kwargs)
        return logged_out_view(request, *args, **kwargs)

    return inner_view


class PageNotFoundView(TemplateView):
    template_name = '404.html'

