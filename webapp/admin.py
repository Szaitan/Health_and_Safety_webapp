from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from webapp.models import CustomerCompany, CustomerCompanyEmails, Project, CustomUser


# Register your models here.


class CustomerCompanyAdmin(admin.ModelAdmin):
    list_filter = ("name", "general_emails")


class CustomerCompanyEmailAdmin(admin.ModelAdmin):
    list_filter = ("email",)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'user_company')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'user_company')}),
    )


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "company")
    list_filter = ('name', "company")


admin.site.register(CustomerCompany, CustomerCompanyAdmin)
admin.site.register(CustomerCompanyEmails, CustomerCompanyEmailAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Project, ProjectAdmin)
