from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django import test as django_test

import Buyabook
from Buyabook.accounts.models import BaBUser, Profile
from Buyabook.books.models import Book


class CatalogueViewTest(django_test.TestCase):

    def test_index_status_code_when_not_logged_in(self):
        response = self.client.get('/catalogue/')
        self.assertEquals(response.status_code, 200)

    def test_index_url_name_when_not_logged_in(self):
        response = self.client.get(reverse('catalogue'))
        self.assertEquals(response.status_code, 200)

    def test_index_correct_template_when_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogue.html')


class MyDashboardTest(django_test.TestCase):
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
        'price': 2.0,
        }
    NEW_VALID_BOOK_DETAILS = {
        'title': 'FirstBook',
        'author': 'Author',
        'price': 3.0,
        }

    def test_when_logged_in_user_tries_to_access_dashboard_expect_success(self):


        user = get_user_model().objects.create_user(**self.VALID_USER_CREDENTIALS)
        user.save()

        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        profile.save()

        self.client.login( **self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse_lazy('index'))
        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'catalogue.html')

    def test_when_logged_in_user_tries_to_delete_their_book__expect_success(self):

        user = get_user_model().objects.create_user(**self.VALID_USER_CREDENTIALS)
        user.save()

        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        profile.save()

        self.assertTrue(self.client.login(**self.VALID_USER_CREDENTIALS))

        book = Book(**self.VALID_BOOK_DETAILS, seller=profile)
        book.save()
        pk = book.pk

        # self.client.logout()

        response = self.client.get(reverse_lazy('delete book', kwargs={
            'pk': pk, }))
        self.assertEquals(response.status_code, 200)

        response = self.client.post(reverse_lazy('delete book', kwargs={'pk': pk, }))
        self.assertEquals(response.status_code, 302)
        self.assertURLEqual(response.url, reverse_lazy('index'))

        with self.assertRaises(Exception) as ex:
            Book.objects.get(pk=pk)
        self.assertEquals(Buyabook.books.models.Book.DoesNotExist, ex.exception.__class__)


    def test_when_logged_in_user_tries_to_update_book__expect_success(self):

        user = get_user_model().objects.create_user(**self.VALID_USER_CREDENTIALS)
        user.save()

        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        profile.save()

        # self.client.login(**self.VALID_SELLER_CREDENTIALS)

        book = Book(**self.VALID_BOOK_DETAILS, seller=profile)

        book.save()
        pk = book.pk

        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse_lazy('update book', kwargs={'pk': pk, }))
        self.assertEquals(response.status_code, 200)

        new_price = 3
        response = self.client.post(
            reverse_lazy('update book', kwargs={'pk': pk, } ),
            data=self.NEW_VALID_BOOK_DETAILS)

        self.assertNotEqual(new_price, book.price)
        book.refresh_from_db()
        self.assertEqual(new_price, book.price)


