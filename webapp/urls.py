from django.urls import path
from . import views

urlpatterns = [
    path("", views.IntroPageView.as_view(), name="intro_page"),
    path("add_user_page", views.AddUserPage.as_view(), name="add_user_page"),
    path("login_page", views.LoginPageView.as_view(), name="login_page"),
    path("logout_page", views.LogoutPage.as_view(), name="logout_page"),
    path("register_page", views.RegisterPageView.as_view(), name="register_page"),
    path("index_page", views.IndexPage.as_view(), name="index_page"),
]
