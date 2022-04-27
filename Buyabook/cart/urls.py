from django.urls import path

from Buyabook.cart.views import CartView, add_to_cart, remove_from_cart

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('buy/<int:pk>/', add_to_cart, name='buy'),
    path('remove/<int:pk>/', remove_from_cart, name='remove'),

]
