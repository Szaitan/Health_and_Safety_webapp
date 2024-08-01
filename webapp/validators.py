# validators.py

import re
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import CustomUser, CustomerCompany, Project


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


def validate_unique_email(value, current_user=None):
    if CustomUser.objects.filter(email=value).exclude(id=current_user.id if current_user else None).exists():
        raise ValidationError("Email is already in use.")


def validate_companies_identification_number(value):
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError("Tax identification number should only contain numbers.")
    if re.search(r'[A-Z]', value):
        raise ValidationError("Tax identification number should only contain numbers.")
    if re.search(r'[a-z]', value):
        raise ValidationError("Tax identification number should only contain numbers.")
    if not CustomerCompany.objects.filter(taxpayer_identification_number=value):
        raise ValidationError("This taxpayer identification number does not exist in database.")
