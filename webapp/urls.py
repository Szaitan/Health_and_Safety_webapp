from django.urls import path
from . import views

urlpatterns = [
    path("", views.IntroPageView.as_view(), name="intro_page"),
    path("login_page", views.LoginPageView.as_view(), name="login_page")
]