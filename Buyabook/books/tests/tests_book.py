from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

from Buyabook.accounts.models import BaBUser, Profile
from Buyabook.books.models import Book


class BookCreateTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': 'testpassword123',
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Testov',
        'email': 'testuser@email.com',
    }

    def test_create_user_with_correct_data__expect_success(self):
        user = BaBUser(**self.VALID_USER_CREDENTIALS)
        user.save()
        self.assertIsNotNone(BaBUser.pk)

    VALID_BOOK_DETAILS = {
        'title': 'FirstBook',
        'author': 'Author',
        'price': '2',
        }

    def test_no_books_in_initial_book_set__expect_success(self):
        user = get_user_model().objects.create_user(**self.VALID_USER_CREDENTIALS)
        user.save()

        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        profile.save()

        self.assertEqual(profile.book_set.count(), 0)

    def test_create_book_from_a_user__expect_success(self):
        user = BaBUser(**self.VALID_USER_CREDENTIALS)
        user.save()
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)

        profile.save()

        Book(**self.VALID_BOOK_DETAILS, seller=profile).save()

        book = Book.objects.get(pk=1)

        self.assertIsNotNone(Book.pk)
        self.assertEquals(book.seller, profile)
        self.assertEquals('FirstBook', book.title)
        self.assertEquals(2.0, book.price)
        self.assertTrue( book.is_available())


class BookEditViewTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
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
        'price': '2',
        }

    def test_edit_book_url_when_seller_wants_to_edit__expect_success(self):

        user = get_user_model().objects.create_user(**self.VALID_USER_CREDENTIALS)
        user.save()

        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        profile.save()

        book = Book(**self.VALID_BOOK_DETAILS, seller=profile)
        book.save()
        pk = book.pk

        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse_lazy('update book', kwargs={
            'pk': pk, }))
        self.assertEquals(response.status_code, 200)
