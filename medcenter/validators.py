from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re


def validate_users(value):
    if not re.fullmatch(r'[a-zA-Z\d]{2,25}', value):
        raise ValidationError(
            _('%(value)s is invalid'),
            params={'value': value},
        )


def validate_email(value):
    if not re.fullmatch(r'[a-zA-Z\d]{5,50}@gmail.com', value):
        raise ValidationError(
            _('%(value)s email is invalid'),
            params={'value': value},
        )


def validate_phone(value):
    if not re.fullmatch(r'(\+\s?)?\d{3}\s?\(\d{2}\)\s?\d{3}(-|\s)?\d{2}(-|\s)?\d{2}', value):
        raise ValidationError(
            _('%(value)s number is invalid'),
            params={'value': value},
        )
