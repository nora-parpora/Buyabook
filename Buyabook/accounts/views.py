

from django.contrib import messages
from django.contrib.auth import views as auth_views, logout
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.http import request, HttpRequest

from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, DeleteView, ListView

from Buyabook.accounts.forms import CreateProfileForm, UpdateProfileForm, DeleteProfileForm
from Buyabook.accounts.helpers import AuthCheckView
from Buyabook.accounts.models import Profile, BaBUser
from Buyabook.books.models import Book



class UserRegisterView(CreateView):
    form_class = CreateProfileForm
    template_name = 'create_profile.html'
    #messages.success(request, f'Successfully created an account!')
    success_url = reverse_lazy('login')



class HomeView(TemplateView):  # Showing the landing page when the user is not logged in.
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_books'] = Book.objects.all()


# class IndexView(TemplateView, AuthCheckView):
#     template_name = 'index.html'
    # def logout_view(self, request):
    #     logout(request)
    #     return redirect('login')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


class DashboardView(ListView, AuthCheckView):
    queryset = Book.objects.all()
    template_name = 'catalogue.html'

    def personal_books(self, obj):
        books = Book.objects.all().filter(owner_id=self.request.user.pk)
        return books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.request.user.id)
        context['profile'] = profile
        context['books'] = Book.objects.filter(owner_id=profile.user.id)
        context['all_books'] = Book.objects.all()


        #books = Book.objects.filter(profile__owner_id=self.request.user.pk)
        #     #'is_owner': self.object.user_id == self.request.user.id,
        return context


class UserLoginView(auth_views.LoginView):
    template_name = 'login_page.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.request.user.id)


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('update profile')


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, pk=self.request.user.id)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.request.user.id)

    #     context.update({
    #         'is_owner': self.object.user_id == self.request.user.id,
    #     })
        return context


class DeleteProfileView(DeleteView):
    model = BaBUser
    #form_class = DeleteProfileForm
    template_name = 'delete_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return get_object_or_404(BaBUser, pk=self.request.user.id)


class UnauthView(TemplateView):
    template_name = '404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def logged_in_switch_view(logged_in_view, logged_out_view):
    def inner_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return logged_in_view(request, *args, **kwargs)
        return logged_out_view(request, *args, **kwargs)

    return inner_view



    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     profile = get_object_or_404(Profile, pk=self.request.user.id)
    #     #user = get_object_or_404(User, pk=self.request.user.id)
    #     context['form'] = self.form_class(instance=profile)
    #     return context



# class DeleteProfileView(DeleteView):
#     model = Profile
#     #form_class = DeleteProfileForm
#     template_name = 'delete_profile.html'
#     success_url = reverse_lazy('login')
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Profile, pk=self.request.user.id)
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     profile = get_object_or_404(Profile, pk=self.request.user.id)
#     #     #user = get_object_or_404(User, pk=self.request.user.id)
#     #     context['form'] = self.form_class(instance=profile)
#     #     return context





# class UpdateProfileView(UpdateView):
#     model = Profile
#     form_class = UpdateProfileForm
#     template_name = 'update_profile.html'
#     success_url = 'index.html'
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = get_object_or_404(Profile, pk=self.kwargs.get('pk')).user
#         profile = Profile.objects.get(pk=user.pk)
#
#         form = self.form_class(instance=profile)
#         context['form'] = form
#         a=5

        # form = self.form_class(instance=user)
        # context['form'] = self.form_class(instance=user)


# class UpdateProfileView(UpdateView):
#     model = Profile
#     fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'address',]
#     template_name = 'update_profile.html'
#     success_url = 'index.html'
#     user = get_object_or_404(Profile, pk=request.user.id
#     user_form = UpdateProfileForm(instance=user.profile.pk)
#
#     def get_object(self, queryset=None):
#         user = get_object_or_404(Profile, pk=request.user.id

    # def get_context_data(self, **kwargs):
    #     user = get_object_or_404(Profile, pk=self.kwargs.get('pk')).user
    #
    #     #context['user_form']= self.user_form_class(instance=user)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     user = get_object_or_404(Profile, pk=self.kwargs.get('pk')).user
    #     #user_form = UserChangeForm(instance=user)
    #     context.update({
    #         'total_likes_count': total_likes_count,
    #         'total_pet_photos_count': total_pet_photos_count,
    #         'is_owner': self.object.user_id == self.request.user.id,
    #         'pets': pets,
    #     })
    #     return context






