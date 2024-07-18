from django.urls import path
from . import views

urlpatterns = [
    path("", views.IntroPageView.as_view(), name="intro_page"),
    path("add_user_to_project_page/<str:project_name>", views.AddUserToProject.as_view(), name="add_user_to_project"),
    path("create_user_page", views.CreateUserPage.as_view(), name="create_user_page"),
    path("index_page", views.IndexPage.as_view(), name="index_page"),
    path("login_page", views.LoginPage.as_view(), name="login_page"),
    path("logout_page", views.LogoutPage.as_view(), name="logout_page"),
    path("projects_page", views.ProjectsPage.as_view(), name="projects_page"),
    path("register_page", views.RegisterPage.as_view(), name="register_page")
]
