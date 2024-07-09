from django.db import models


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


