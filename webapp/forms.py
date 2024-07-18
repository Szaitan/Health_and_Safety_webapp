from django import forms
from django.core import validators
from .models import CustomerCompany, Project, CustomUser
from .validators import validate_password, validate_unique_email


class CreateUserForm(forms.Form):
    # project = forms.ModelChoiceField(queryset=Project.objects.none())
    first_name = forms.CharField(min_length=1, max_length=35)
    last_name = forms.CharField(min_length=1, max_length=50)
    company = forms.CharField(min_length=1, max_length=50)
    email = forms.EmailField(validators=[validators.EmailValidator, validate_unique_email])
    user_type = forms.ChoiceField(choices=(("base_user", "Base User"), ("hse_inspector", "HSE Inspector"),
                                           ("project_manager", "Project Manager")))
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(AddUserForm, self).__init__(*args, **kwargs)
    #     if user:
    #         self.fields['project'].queryset = Project.objects.filter(customuser=user)


class AddUsertoProject(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.none())

    def __init__(self, *args, **kwargs):
        super(AddUsertoProject, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.all()


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
