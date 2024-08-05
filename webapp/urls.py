from django.urls import path
from . import views

urlpatterns = [
    path("", views.IntroPageView.as_view(), name="intro_page"),
    path("add_user_to_project_page/<slug:project_slug>", views.AddUserToProject.as_view(), name="add_user_to_project"),
    path("card_and_incident", views.CardAndIncidentPage.as_view(), name="card_and_incident_page"),
    path("create_project_page", views.CreateProjectPage.as_view(), name="create_project_page"),
    path("create_user_page", views.CreateUserPage.as_view(), name="create_user_page"),
    path("edit_user_page", views.EditUserPage.as_view(), name="edit_user_page"),
    path("index_page", views.IndexPage.as_view(), name="index_page"),
    path("login_page", views.LoginPage.as_view(), name="login_page"),
    path("logout_page", views.LogoutPage.as_view(), name="logout_page"),
    path("project_database", views.ProjectDatabasePage.as_view(), name="project_database"),
    path("projects_page", views.ProjectsPage.as_view(), name="projects_page"),
    path("register_page", views.RegisterPage.as_view(), name="register_page"),
    path("remove_user_from_project", views.RemoveUserFromProjects.as_view(), name="remove_user_from_project")
]

