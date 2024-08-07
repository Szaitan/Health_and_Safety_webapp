from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from webapp.models import CardAndIncident, CustomerCompany, CustomerCompanyEmails, Project, CustomUser,\
    ProjectDatabase


# Register your models here.

class CardAndIncidentAdmin(admin.ModelAdmin):
    list_filter = ("project", "contractor", "subcontractor", "name_surname", "issued_card")
    list_display = ("project", "contractor", "subcontractor", "name_surname", "issued_card")


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


class ProjectDatabaseAdmin(admin.ModelAdmin):
    list_display = ("project", "contractor", "subcontractor", "date")
    list_filter = ('project', "contractor", "subcontractor", "date")


admin.site.register(CardAndIncident, CardAndIncidentAdmin)
admin.site.register(CustomerCompany, CustomerCompanyAdmin)
admin.site.register(CustomerCompanyEmails, CustomerCompanyEmailAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectDatabase, ProjectDatabaseAdmin)
