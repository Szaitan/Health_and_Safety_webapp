import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect, render, reverse
from django.views import View
from .views_functions import register_send_email
from webapp.forms import AddUsertoProject, CreateProjectForm, CreateUserForm, EditUserForm, LoginForm, RegisterForm
from .models import CustomerCompany, CustomUser, Project


# Create your views here.

def get_year():
    return datetime.datetime.today().year


class AddUserToProject(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type not in ['hse_inspector', 'project_manager', 'company_representative']:
            return redirect(reverse('intro_page'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, project_name):
        form = AddUsertoProject()
        return render(request, "webapp/add_user_to_project_page.html",
                      {"project_name": project_name,
                       "form": form,
                       })

    def post(self, request, project_name):
        form = AddUsertoProject(request.POST)
        if form.is_valid():
            project = Project.objects.get(name=project_name)
            project.user.add(form.cleaned_data["user"])
            project.save()
            return render(request, 'webapp/add_user_to_project_page.html', {
                "project_name": project_name,
                'form': form,
                'message': f"User {form.cleaned_data['user']} has been successfully added to project {project.name}"
            })
        return render(request, 'webapp/add_user_to_project_page.html', {
            "project_name": project_name,
            "form": form
        })


class CreateProjectPage(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type not in ['company_representative']:
            return redirect(reverse('intro_page'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, reqeust):
        form = CreateProjectForm()
        return render(reqeust, "webapp/create_project_page.html", {
            "form": form,
            "year": get_year()
        })

    def post(self, request):
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            form_clean_data = form.cleaned_data
            project_name = form_clean_data["name"]
            user_company = CustomerCompany.objects.get(name=request.user.user_company)
            project = Project.objects.create(name=project_name, company=user_company)
            project.user.set([request.user])
            return render(request, "webapp/create_project_page.html", {
                "form": form,
                "year": get_year(),
                "message": f"Project: {project_name} created successfully"
            })
        return render(request, "webapp/create_project_page.html", {
            "form": form,
            "year": get_year()
        })


# Intro Page View
class CreateUserPage(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type not in ['hse_inspector', 'project_manager', 'company_representative']:
            return redirect(reverse('intro_page'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = CreateUserForm()
        return render(request, "webapp/create_user_page.html", {
            "form": form,
            "year": get_year()
        })

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Create the new user
            user = CustomUser.objects.create_user(username=form.cleaned_data["email"].split('@')[0],
                                                  email=form.cleaned_data["email"],
                                                  user_company=form.cleaned_data["company"],
                                                  password=form.cleaned_data["password"],
                                                  first_name=form.cleaned_data["first_name"],
                                                  last_name=form.cleaned_data["last_name"],
                                                  user_type=form.cleaned_data["user_type"])
            user.save()
            return redirect("projects_page")
        return render(request, "webapp/create_user_page.html", {
            "form": form,
            "year": get_year(),
        })


class EditUserPage(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(CustomUser, id=request.user.id)
        form = EditUserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'company': user.user_company,
            'email': user.email
        }, current_user=request.user)
        return render(request, "webapp/edit_user_page.html", {
            "form": form,
            "year": get_year()
        })

    def post(self, request):
        user = get_object_or_404(CustomUser, id=request.user.id)
        form = EditUserForm(request.POST, current_user=request.user)
        if form.is_valid():
            form_clean_data = form.cleaned_data
            # Updating user data
            user.first_name = form_clean_data["first_name"]
            user.last_name = form_clean_data["last_name"]
            user.user_company = form_clean_data["company"]
            user.email = form_clean_data["email"]
            if not form_clean_data["password"] == "":
                user.password = form_clean_data["password"]
            user.save()

            messages.success(request, "User updated successfully")
            return redirect('index_page')
        return render(request, "webapp/edit_user_page.html", {
            "form": form,
            "year": get_year()
        })


class IndexPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "webapp/index_page.html", {
            "year": get_year()
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


class LoginPage(View):
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

            return render(request, "webapp/login_page.html", {
                "form": LoginForm(),
                "year": get_year()})

        return redirect(reverse("login_page"))


class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect("intro_page")


class RegisterPage(View):
    def get(self, request):
        return render(request, "webapp/register_page.html", {
            "form": RegisterForm(),
            "year": get_year()
        })

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data

            # customer_companies_emails_query_list = [email for email in CustomerCompanyEmails.objects.filter(
            #     customercompany__name=clean_data["customer_companies"].name).values_list('email', flat=True)]
            # register_send_email(clean_data["customer_companies"].name, clean_data["first_name"], clean_data["last_name"],
            #                     clean_data["company"], clean_data["email"], customer_companies_emails_query_list)

            return render(request, 'webapp/register_page.html', {
                'form': form,
                'message': f"Your registration was successfully sent to verification."
            })

        return render(request, "webapp/register_page.html", {
            "form": form,
            "year": get_year()})


class ProjectsPage(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type not in ['hse_inspector', 'project_manager', 'company_representative']:
            return redirect(reverse('intro_page'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        projects_data = Project.objects.filter(user=request.user)
        return render(request, "webapp/projects_page.html", {
            "projects_data": projects_data,
            "title": "- Projects Page",
            "year": get_year()
        })


class RemoveUserFromProjects(LoginRequiredMixin, View):
    def post(self, request):
        project_name = request.POST.get("project_name")
        user_id = request.POST.get("user_id")

        project = get_object_or_404(Project, name=project_name)
        user = get_object_or_404(CustomUser, id=user_id)

        project.user.remove(user)
        return JsonResponse({'success': True})
