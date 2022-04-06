from django.contrib.auth import views as auth_views, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from Buyabook.accounts.forms import CreateProfileForm
from Buyabook.accounts.helpers import AuthCheckView


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


class UnauthView(TemplateView):
    template_name = '404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

