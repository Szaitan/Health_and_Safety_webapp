import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from .views_functions import register_send_email
from webapp.forms import AddUsertoProject, CreateProjectForm, CreateUserForm, EditUserForm, LoginForm, RegisterForm,\
    CardAndIncidentForm, ProjectDatabaseForm, SiteObservationReportForm
from .models import CardAndIncident, CustomerCompany, CustomerCompanyEmails, CustomUser, Project, ProjectDatabase


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

    def get(self, request, project_slug):
        form = AddUsertoProject()
        project = get_object_or_404(Project, slug=project_slug)
        return render(request, "webapp/add_user_to_project_page.html", {
            "project_slug": project_slug,
            "project_name": project.name,
            "form": form,
        })

    def post(self, request, project_slug):
        form = AddUsertoProject(request.POST)
        project = get_object_or_404(Project, slug=project_slug)
        if form.is_valid():
            project.user.add(form.cleaned_data["user"])
            project.save()
            return render(request, 'webapp/add_user_to_project_page.html', {
                "project_name": project.name,
                "project_slug": project_slug,
                "form": form,
                "message": f"User {form.cleaned_data['user']} has been successfully added to project {project.name}"
            })
        return render(request, 'webapp/add_user_to_project_page.html', {
            "project_name": project.name,
            "form": form
        })


# Page for creation of cards
class CardAndIncidentPage(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type not in ['hse_inspector', 'project_manager', 'company_representative']:
            return redirect(reverse('intro_page'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = CardAndIncidentForm(current_user=request.user)
        return render(request, "webapp/card_and_incident_page.html", {
            "form": form,
            "year": get_year(),
        })

    def post(self, request):
        form = CardAndIncidentForm(request.POST, current_user=request.user)
        if form.is_valid():
            form_data = form.cleaned_data

            CardAndIncident.objects.create(
                project=form_data["project"],
                contractor=form_data["contractor"].lower(),
                subcontractor=form_data["subcontractor"].lower(),
                name_surname=form_data["name_surname"].lower(),
                date=form_data["date"],
                year=int(form_data["date"].year),
                month=int(form_data["date"].month),
                week=f"{form_data['date'].strftime('%W')} of {form_data['date'].year}",
                type=form_data["type"],
                description=form_data["description"],
                issued_card=form_data["issued_card"]
            )
            return redirect(reverse('index_page'))

        return render(request, "webapp/card_and_incident_page.html", {
            "form": form,
            "year": get_year(),
        })


class CreateProjectPage(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type not in ['company_representative']:
            return redirect(reverse('intro_page'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = CreateProjectForm(current_user=request.user)
        return render(request, "webapp/create_project_page.html", {
            "form": form,
            "year": get_year()
        })

    def post(self, request):
        form = CreateProjectForm(request.POST, current_user=request.user)

        if form.is_valid():
            # Checking number of projects
            user_company_name = request.user.user_company
            user_company = CustomerCompany.objects.get(name=user_company_name)
            current_num_projects = Project.objects.filter(company=user_company)
            if user_company.num_of_projects == current_num_projects.count():
                return render(request, "webapp/create_project_page.html", {
                    "form": form,
                    "year": get_year(),
                    "message": "Total number of projects reached maximum. Please buy more project slots."
                })

            # Creation of project
            form_clean_data = form.cleaned_data
            project_name = form_clean_data['name']
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
                                                  user_company=form.cleaned_data["company"].lower(),
                                                  password=form.cleaned_data["password"],
                                                  first_name=form.cleaned_data["first_name"],
                                                  last_name=form.cleaned_data["last_name"],
                                                  user_type=form.cleaned_data["user_type"])
            user.save()
            return render(request, "webapp/create_user_page.html", {
                "form": form,
                "year": get_year(),
                "message": f"User {form.cleaned_data['first_name']} {form.cleaned_data['last_name']} "
                           f"created successfully."})
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
            'company': user.user_company.capitalize(),
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
            user.user_company = form_clean_data["company"].lower()
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
        return render(request, "webapp/intro_page.html", {
            "year": get_year()
        })


class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index_page")
        return render(request, "webapp/login_page.html", {
            "form": LoginForm(),
            "year": get_year()
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(username=clean_data["email"], password=clean_data["password"])
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


class ProjectDatabasePage(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type not in ['hse_inspector', 'project_manager', 'company_representative']:
            return redirect(reverse('intro_page'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = ProjectDatabaseForm(current_user=request.user)
        return render(request, "webapp/project_database_page.html", {
            "form": form,
            "year": get_year()
        })

    def post(self, request):
        form = ProjectDatabaseForm(request.POST, current_user=request.user)
        if form.is_valid():
            project_database_clean_data = form.cleaned_data
            ProjectDatabase.objects.create(
                project=project_database_clean_data["project"],
                contractor=project_database_clean_data["contractor"],
                subcontractor=project_database_clean_data["subcontractor"],
                date=project_database_clean_data["date"],
                year=project_database_clean_data["date"].year,
                month=project_database_clean_data["date"].month,
                week=f"{project_database_clean_data['date'].strftime('%W')} of {project_database_clean_data['date'].year}",
                average_number_people=project_database_clean_data["average_number_people"],
                hours_work=project_database_clean_data["hours_work"],
            )
            return render(request, "webapp/project_database_page.html", {
                "form": form,
                "message": "Your database has been updated.",
                "year": get_year()
            })
        return render(request, "webapp/project_database_page.html", {
            "form": form,
            "year": get_year()
        })


class ProjectsPage(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type not in ['hse_inspector', 'project_manager', 'company_representative']:
            return redirect(reverse('intro_page'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        projects_data = Project.objects.filter(user=request.user).order_by("name")

        # We are adding new attribute 'users_sorted' which will allow to display them in order.
        for project in projects_data:
            project.users_sorted = project.user.all().order_by('first_name', 'last_name')

        return render(request, "webapp/projects_page.html", {
            "projects_data": projects_data,
            "title": "- Projects Page",
            "year": get_year()
        })


class RemoveUserFromProjects(LoginRequiredMixin, View):
    def post(self, request):
        slug = request.POST.get("slug")
        user_id = request.POST.get("user_id")

        project = get_object_or_404(Project, slug=slug)
        user = get_object_or_404(CustomUser, id=user_id)

        project.user.remove(user)
        # If this is the last user in project, project will be removed plus information regarding removing user.
        if not project.user.exists():
            project.delete()
        return JsonResponse({'success': True})


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
            # Preparation of list which containes email adress connected to this company tax id
            customer_companies_emails_query_list = [email for email in CustomerCompanyEmails.objects.filter(
                customercompany__taxpayer_identification_number=
                clean_data["company_tax_identification_number"]).values_list('email', flat=True)]

            # Company object for company name
            company_object = CustomerCompany.objects.get(taxpayer_identification_number=
                                                         clean_data["company_tax_identification_number"])

            # Sending email with user form for registration to filtrated emails
            register_send_email(company_object.name, clean_data["first_name"],
                                clean_data["last_name"], clean_data["company"],
                                clean_data["email"], customer_companies_emails_query_list)

            return render(request, 'webapp/register_page.html', {
                'form': form,
                'message': f"Your registration was successfully sent to verification."
            })

        return render(request, "webapp/register_page.html", {
            "form": form,
            "year": get_year()})


class SiteObservationReportPage(View):
    def get(self, request):
        form = SiteObservationReportForm(current_user=request.user)
        return render(request, "webapp/site_observation_report_page.html", {
            "form": form,
            "year": get_year(),
        })

    def post(self, request):
        form = SiteObservationReportForm(request.POST, current_user=request.user)
        print("here")
        print(form.errors)
        if form.is_valid():
            print(form.cleaned_data["head_protection"])
            print(form.cleaned_data["loto"])
            print(form.cleaned_data["date"])
            return render(request, "webapp/site_observation_report_page.html", {
                "form": form,
                "year": get_year(),
            })
        return render(request, "webapp/site_observation_report_page.html", {
            "form": form,
            "year": get_year(),
        })
