from django.contrib.auth import get_user_model
from django import test as django_test
from django.core.exceptions import ValidationError

from Buyabook.accounts.models import Profile, BaBUser

UserModel = get_user_model()


class UserProfileDetailsModelTest(django_test.TestCase):
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

    def test_create_profile_with_correct_data__expect_success(self):
        user = BaBUser.objects.create_user(**self.VALID_USER_CREDENTIALS)
        user.save()
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        profile.save()
        self.assertIsNotNone(BaBUser.pk)
        self.assertIsNotNone(Profile.pk)

        printed_name = 'Test Testov'
        self.assertEqual(printed_name, str(profile))


    def test_create_user_with_incorrect_data__expect_password_validationerror(self):
        user = BaBUser(username='t2222222222222222222222222222222222222222221', password='password123',)
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
            user.save()
        self.assertIsNotNone(context.exception)

    def test_create_profile_with_incorrect_data_in_first_name__expect_failure(self):
        user = BaBUser.objects.create_user(**self.VALID_USER_CREDENTIALS)
        user.save()
        profile = Profile.objects.create(first_name='Test1', last_name='Testov', email='test@test.com', user=user)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)


    def test_create_profile_with_incorrect_data_in_last_name__expect_failure(self):
        user = BaBUser.objects.create_user(**self.VALID_USER_CREDENTIALS)
        user.save()
        profile = Profile.objects.create(first_name='Test', last_name='Test&', email='test@test.com', user=user)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)


    def test_create_profile_with_incorrect_data_in_email_name__expect_failure(self):
        user = BaBUser.objects.create_user(**self.VALID_USER_CREDENTIALS)
        user.save()
        profile = Profile.objects.create(first_name='Test', last_name='Testov', email='test.test.com', user=user)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)
