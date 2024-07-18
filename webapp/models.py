from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
# Emails connected to CustomerCompany model, which will be selected as designated email during registration.
class CustomerCompanyEmails(models.Model):
    email = models.EmailField()

    def __str__(self):
        return f"{self.email}"


class CustomerCompany(models.Model):
    name = models.CharField(max_length=75)
    general_emails = models.ManyToManyField(CustomerCompanyEmails)

    def __str__(self):
        return f"{self.name}"


# It's my CustomUser
class CustomUserManager(BaseUserManager):
    # Do update przy formularzu, który będzie tworzył usera
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email, )
        user = self.model(username=username.strip(), email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=20, choices=(("base_user", "Base User"),
                                                         ("hse_inspector", "HSE Inspector"),
                                                         ("project_manager", "Project Manager")))
    user_company = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Project(models.Model):
    name = models.CharField(max_length=30, unique=True)
    company = models.ForeignKey(CustomerCompany, on_delete=models.CASCADE)
    user = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return f"{self.name}"
