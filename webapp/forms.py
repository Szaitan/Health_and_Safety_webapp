from django import forms
from django.core import validators
from .models import CustomerCompany, Project, CustomUser
from .validators import validate_password, validate_unique_email, validate_unique_project_name
from .model_functions import generate_password


class AddUsertoProject(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.none())

    def __init__(self, *args, **kwargs):
        super(AddUsertoProject, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.all()


class CreateProjectForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=40, validators=[validate_unique_project_name])


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
    password = forms.CharField(validators=[validate_password], required=False, help_text="In case, change password.")

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
    customer_companies = forms.ModelChoiceField(
        queryset=CustomerCompany.objects.all(),
        widget=forms.Select,
    )
    first_name = forms.CharField(min_length=1, max_length=35)
    last_name = forms.CharField(min_length=1, max_length=50)
    company = forms.CharField(min_length=1, max_length=50)
    email = forms.EmailField(validators=[validators.EmailValidator, validate_unique_email])
