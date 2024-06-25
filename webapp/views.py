from django.shortcuts import render, reverse, redirect
from django.views import View
import datetime


# Create your views here.

def get_year():
    return datetime.datetime.today().year


# Intro Page View
class IntroPageView(View):
    def get(self, request):
        return render(request, 'webapp/intro_page.html', {
            "year": get_year()
        })
