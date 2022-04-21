from django.core.exceptions import ValidationError


def validate_add_to_cart_perm(value, *args, **kwargs):
    if value.seller.pk == value.cart.pk:
        raise ValidationError("The Buyer cannot be the same as the Seller")