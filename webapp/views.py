from django.shortcuts import render, reverse, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .views_functions import register_send_email
from webapp.forms import LoginForm, RegisterForm, AddUserForm
from .models import CustomerCompanyEmails, CustomUser
import datetime


# Create your views here.

def get_year():
    return datetime.datetime.today().year


# Intro Page View
class AddUserPage(LoginRequiredMixin, View):
    def get(self, request):
        form = AddUserForm(user=request.user)
        return render(request, "webapp/add_user_page.html", {
            "form": form,
            "year": get_year()
        })

    def post(self, request):
        form = AddUserForm(request.POST, user=request.user)
        print(form.errors)
        if form.is_valid():
            project = form.cleaned_data["project"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            company = form.cleaned_data["company"]
            email = form.cleaned_data["email"]
            user_type = form.cleaned_data["user_type"]
            password = form.cleaned_data["password"]
            print(project)
            print(type(project.name))
            print(first_name)
            print(last_name)
            print(company)
            print(email)
            print(user_type)
            print(password)
            # Create the new user
            user = CustomUser.objects.create_user(username=email.split('@')[0], email=email,
                                                  password=password, first_name=first_name,
                                                  last_name=last_name, user_type=user_type)
            user.user_projects.add(project)
            user.save()
            return redirect("add_user_page")
        return render(request, "webapp/add_user_page.html", {
            "form": form,
            "year": get_year(),
        })


class IntroPageView(View):
    def get(self, request):
        # Test to check about user
        # if request.user.is_authenticated:
        #     print(request.user.user_projects.all()[0].name)

        # Test with creation of superuser
        # CustomUser.objects.create_user(username="test2", email="", password="",
        #                                first_name="Dupa", last_name="Dupp", user_type="normal")
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
        form = LoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(username=clean_data["email"], password=clean_data["password"])
            print(clean_data["email"], clean_data["password"])
            if user is not None:
                login(request, user)
                return redirect("index_page")
            else:
                print("Nope")

            return render(request, "webapp/login_page.html", {
                "form": LoginForm(),
                "year": get_year()}
                          )

        return redirect(reverse("login_page"))


class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect("intro_page")


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


class IndexPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "webapp/index_page.html", {
            "year": get_year()
        })
