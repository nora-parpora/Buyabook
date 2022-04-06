from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from Buyabook.accounts.views import IndexView, UserRegisterView, UserLoginView, UnauthView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),


    path('404/', UnauthView.as_view(), name='404'),

]