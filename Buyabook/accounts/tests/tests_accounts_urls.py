from django.contrib.auth import get_user_model
from django import test as django_test
from django.core.exceptions import ValidationError
from django.urls import reverse

from Buyabook.accounts.models import Profile, BaBUser

UserModel = get_user_model()


class IndexPageTest(django_test.TestCase):

    def test_index_status_code_when_not_logged_in(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_index_url_name_when_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)

    def test_index_correct_template_when_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogue.html')

    def test_register_status_code(self):
        response = self.client.get('/accounts/register/')
        self.assertEquals(response.status_code, 200)

    def test_register_url_name(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)

    def test_register_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_profile.html')
