# validators.py

import re
from django.core.exceptions import ValidationError
from .models import CustomUser


def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Password must contain at least 8 characters.")
    if not re.search(r'[A-Z]', value):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', value):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', value):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError("Password must contain at least one special character.")


def validate_unique_email(value):
    if CustomUser.objects.filter(email=value).exists():
        raise ValidationError("Email is already in use.")