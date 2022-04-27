from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404

from django.views.generic import ListView

from Buyabook.accounts.helpers import CurrentUserView
from Buyabook.books.models import Book
from Buyabook.cart.models import Cart


class CartView(LoginRequiredMixin, ListView, CurrentUserView):
    model = Book
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        cart_total = sum([b.price for b in Book.objects.filter(cart_id=self.request.user.id)])
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(cart_id=self.request.user.id)
        context['cart_total'] = cart_total
        return context


def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, pk=pk)
    cart = get_object_or_404(Cart, pk=request.user.id)

    if not book.is_available() or book.seller.pk == request.user.pk:  # cart.user.pk != request.user.pk: /
        # book.seller == request.user.id:  #  not book.seller == request.user.id: #  or request.user.pk == book.cart_id:
        return redirect('404')
    #  TODO elif msg the user that the book is already in the cart

    cart.book_set.add(book)
    cart.save()
    return redirect('cart')


def remove_from_cart(request, pk):
    if not request.user.is_authenticated:  # TODO refactor into separate function
        return redirect('login')

    book = get_object_or_404(Book, pk=pk)
    if book.cart_id == request.user.id or book.seller_id == request.user.id:
        cart = get_object_or_404(Cart, pk=book.cart_id)
        # book.cart_id = None
        cart.book_set.remove(book)
        cart.save()
        if book.cart_id == request.user.id:
            return redirect('cart')
        return redirect('retrieve book')

