from django.urls import path
from . import views

urlpatterns = [
    path("", views.IntroPageView.as_view(), name="intro_page")
]