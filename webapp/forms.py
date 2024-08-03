from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from .models import CustomerCompany, Project, CustomUser
from .validators import (validate_password, validate_unique_email, validate_companies_identification_number)
from .model_functions import generate_password


class AddUsertoProject(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.none())

    def __init__(self, *args, **kwargs):
        super(AddUsertoProject, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.all()


class CardAndIncidentForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.none(),
                                     help_text="Select a project for your card:")
    contractor = forms.CharField(max_length=60, help_text="Select contractor:")
    subcontractor = forms.CharField(max_length=60, help_text="Select subcontractor:")
    name_surname = forms.CharField(max_length=80, help_text="Name and Surname of person:")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), help_text="Select date:")
    type = forms.ChoiceField(choices=(
        ("alcohol", "Alcohol"),
        ("hazard_situation", "Hazard Situation"),
        ("near_miss", "Near Miss"),
        ("positive_observation", "Positive Observation")
    ), help_text="Select type of observation:")
    issued_card = forms.ChoiceField(choices=(
        ("black", "Black"),
        ("green", "Green"),
        ("red", "Red"),
        ("yellow", "Yellow")
    ), help_text="Select card:")
    description = forms.CharField(max_length=100,
                                  widget=forms.Textarea(attrs={'style': 'resize: none;'}),
                                  help_text="Describe observed situation:")

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(CardAndIncidentForm, self).__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(user=self.current_user).order_by("name")


class CreateProjectForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=40)

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(CreateProjectForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name').lower()
        user_company_name = self.current_user.user_company
        try:
            user_company = CustomerCompany.objects.get(name=user_company_name)
        except CustomerCompany.DoesNotExist:
            raise ValidationError(f"Company with name {user_company_name} does not exist.")

        if Project.objects.filter(name=name, company=user_company).exists():
            raise ValidationError(f"A project with the name '{name}' already exists in your company.")

        return name


class CreateUserForm(forms.Form):
    first_name = forms.CharField(min_length=1, max_length=35)
    last_name = forms.CharField(min_length=1, max_length=50)
    company = forms.CharField(min_length=1, max_length=50)
    email = forms.EmailField(validators=[validate_unique_email])
    user_type = forms.ChoiceField(choices=(("base_user", "Base User"), ("hse_inspector", "HSE Inspector"),
                                           ("project_manager", "Project Manager"),
                                           ("company_representative", "Company Representative")))
    password = forms.CharField(validators=[validate_password])

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password'].initial = generate_password()
        self.fields['user_type'].choices = [choice for choice in self.fields['user_type'].choices
                                            if choice[0] != "company_representative"]


class EditUserForm(forms.Form):
    first_name = forms.CharField(min_length=1, max_length=35)
    last_name = forms.CharField(min_length=1, max_length=50)
    company = forms.CharField(min_length=1, max_length=50)
    email = forms.EmailField()
    password = forms.CharField(validators=[validate_password], required=False,
                               help_text="Leave empty, to not change password")

    def __init__(self, *args, **kwargs):
        #  We need to catch argument that is passed to form, or we will have an error
        self.current_user = kwargs.pop('current_user', None)
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = '<span class="help-text">%s</span>' % self.fields['password'].help_text

    def clean_email(self):
        # Allows to additionally affect email field with for example: validators
        email = self.cleaned_data.get('email')
        validate_unique_email(email, self.current_user)
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(validators=[validators.EmailValidator])
    password = forms.CharField(min_length=1, widget=forms.PasswordInput)


# Register form allow people to  fill the template which will be sent to customer companies email/or emails asking
# to be added.
class RegisterForm(forms.Form):
    company_tax_identification_number = forms.CharField(validators=[validate_companies_identification_number])
    first_name = forms.CharField(min_length=1, max_length=35)
    last_name = forms.CharField(min_length=1, max_length=50)
    company = forms.CharField(min_length=1, max_length=50)
    email = forms.EmailField(validators=[validators.EmailValidator, validate_unique_email])
