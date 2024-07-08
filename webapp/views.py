from django.shortcuts import render, reverse, redirect
from django.views import View
from webapp.forms import LoginForm
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
