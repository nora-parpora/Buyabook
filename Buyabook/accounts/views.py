from django.contrib.auth import views as auth_views, logout
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, DeleteView

from Buyabook.accounts.forms import CreateProfileForm, UpdateProfileForm, DeleteProfileForm
from Buyabook.accounts.helpers import AuthCheckView
from Buyabook.accounts.models import Profile, BaBUser


class UserRegisterView(CreateView):
    form_class = CreateProfileForm
    template_name = 'create_profile.html'
    success_url = reverse_lazy('index')


class IndexView(TemplateView, AuthCheckView):
    template_name = 'index.html'

    def logout_view(self, request):
        logout(request)
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(BaBUser, pk=self.request.user.id)

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


class UnauthView(TemplateView):
    template_name = '404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



