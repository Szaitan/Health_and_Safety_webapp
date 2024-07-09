from django.contrib import admin
from webapp.models import CustomerCompany, CustomerCompanyEmails


# Register your models here.

class CustomerCompanyAdmin(admin.ModelAdmin):
    list_filter = ("name", "general_emails")


class CustomerCompanyEmailAdmin(admin.ModelAdmin):
    list_filter = ("email",)


admin.site.register(CustomerCompany, CustomerCompanyAdmin)
admin.site.register(CustomerCompanyEmails, CustomerCompanyEmailAdmin)