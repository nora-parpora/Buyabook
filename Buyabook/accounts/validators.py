from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for letter in value:
        if not letter.isalpha():
            raise ValidationError(f'Username should consist of only of letters')
