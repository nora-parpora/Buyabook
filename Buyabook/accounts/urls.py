from django.contrib.auth.views import LogoutView
from django.urls import path


from Buyabook.accounts.views import UserRegisterView, UserLoginView, UnauthView, \
    UpdateProfileView, ChangeUserPasswordView, ProfileDetailsView, DeleteProfileView, PageNotFoundView

urlpatterns = [

    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalogue'), name='logout'),
    path('update/', UpdateProfileView.as_view(), name='update profile'),
    path('update-password/', ChangeUserPasswordView.as_view(), name='update password'),
    path('details/', ProfileDetailsView.as_view(), name='profile details'),
    path('delete/', DeleteProfileView.as_view(), name='delete profile'),


    path('401/', UnauthView.as_view(), name='401'),
    path('404/', PageNotFoundView.as_view(), name='404'),

]
