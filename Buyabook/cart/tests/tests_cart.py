

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse

import Buyabook
from Buyabook.accounts.models import Profile
from Buyabook.books.models import Book
from Buyabook.cart.models import Cart


class CartTest(django_test.TestCase):
    VALID_SELLER_CREDENTIALS = {
        'username': 'testuser',
        'password': 'testpassword123',
    }
    VALID_BUYER_CREDENTIALS = {
        'username': 'testuser2',
        'password': 'testpassword123',
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Testov',
        'email': 'testuser@email.com',
    }
    VALID_BOOK_DETAILS = {
        'title': 'FirstBook',
        'author': 'Author',
        'price': 2.0,
        }

    def test_add_to_cart__expect_success(self):
        seller = get_user_model().objects.create_user(**self.VALID_SELLER_CREDENTIALS)
        seller.save()

        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=seller)
        profile.save()

        book = Book(**self.VALID_BOOK_DETAILS, seller=profile)
        book.save()
        self.assertTrue(book.is_available())

        buyer = get_user_model().objects.create_user(**self.VALID_BUYER_CREDENTIALS)

        cart = Cart.objects.create(pk=buyer.pk)
        self.assertIsNotNone(cart)
        cart.save()
        self.assertEqual(0, cart.book_set.count())

        self.client.login(**self.VALID_BUYER_CREDENTIALS)
        response = self.client.get(reverse_lazy('buy', kwargs={'pk': book.pk}))
        self.assertEqual(302, response.status_code)
        self.assertURLEqual(reverse('cart'), response.url)


    def test_buyer_add_to_cart_own_book__expect_success(self):
        user = get_user_model().objects.create_user(**self.VALID_SELLER_CREDENTIALS)
        user.save()

        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        profile.save()

        book = Book(**self.VALID_BOOK_DETAILS, seller=profile)
        book.save()
        self.assertTrue(book.is_available())

        cart = Cart.objects.create(pk=user.pk)
        self.assertIsNotNone(cart)
        cart.save()
        self.assertEqual(0, cart.book_set.count())

        self.client.login(**self.VALID_SELLER_CREDENTIALS)
        response = self.client.get(reverse_lazy('buy', kwargs={'pk': book.pk}))
        self.assertEqual(302, response.status_code)
        self.assertURLEqual(reverse('404'), response.url)


