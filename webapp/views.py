from django.shortcuts import render, reverse, redirect
from django.views import View
from .views_functions import register_send_email
from webapp.forms import LoginForm, RegisterForm
from .models import CustomerCompany, CustomerCompanyEmails
import datetime


# Create your views here.

def get_year():
    return datetime.datetime.today().year


# Intro Page View
class IntroPageView(View):
    def get(self, request):
        return render(request, "webapp/intro_page.html", {
            "year": get_year()
        })


class LoginPageView(View):
    def get(self, request):
        return render(request, "webapp/login_page.html", {
            "form": LoginForm(),
            "year": get_year()
        })

    def post(self, request):
        #  To be added after database classes are finished
        return redirect(reverse("login_page"))


class RegisterPageView(View):
    def get(self, request):
        return render(request, "webapp/register_page.html", {
            "form": RegisterForm(),
            "year": get_year()
        })

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            customer_companies_emails_query_list = [email for email in CustomerCompanyEmails.objects.filter(
                customercompany__name=clean_data["customer_companies"].name).values_list('email', flat=True)]
            register_send_email(clean_data["customer_companies"].name, clean_data["name"], clean_data["last_name"],
                                clean_data["company"], clean_data["email"], customer_companies_emails_query_list)

        return render(request, "webapp/register_page.html", {
            "form": RegisterForm(),
            "year": get_year()
        })
