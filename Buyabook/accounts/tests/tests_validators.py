from django import test as django_test
from django.core.exceptions import ValidationError

from Buyabook.accounts.validators import validate_only_letters


class TestValidators(django_test.TestCase):
    def test_validate_only_letters__happy_case(self):
        name = 'abcd'
        result = validate_only_letters(name) == None
        self.assertEquals(True, result)

    def test_validate_only_letters__with_digit__expect_failure(self):
        name = 'abcd1'
        with self.assertRaises(ValidationError) as context:
            validate_only_letters(name)
        self.assertEqual("['Username should consist only of letters']", str(context.exception))


    def test_validate_only_letters__with_symbol__expect_failure(self):
        name = 'abcd&'
        with self.assertRaises(ValidationError) as context:
            validate_only_letters(name)
        self.assertEqual("['Username should consist only of letters']", str(context.exception))


