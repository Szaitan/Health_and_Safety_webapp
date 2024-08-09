from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from .models import CustomerCompany, Project, CustomUser
from .validators import (validate_password, validate_unique_email, validate_companies_identification_number)
from .model_functions import generate_password


class AddUsertoProject(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.none(), help_text="Select user from list to add:")

    def __init__(self, *args, **kwargs):
        super(AddUsertoProject, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.all()


class CardAndIncidentForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.none(),
                                     help_text="Select a project for your card:")
    contractor = forms.CharField(max_length=60, help_text="Contractor name:")
    subcontractor = forms.CharField(max_length=60, help_text="Subcontractor name:")
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
    name = forms.CharField(min_length=1, max_length=40, help_text="Name of the project:")

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(CreateProjectForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        # Instead of passing variables to validator, we can make validation inside clean_name
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
    first_name = forms.CharField(min_length=1, max_length=35, help_text="User first name:")
    last_name = forms.CharField(min_length=1, max_length=50, help_text="User last name:")
    company = forms.CharField(min_length=1, max_length=50, help_text="User company:")
    email = forms.EmailField(validators=[validate_unique_email], help_text="User email:")
    user_type = forms.ChoiceField(choices=(("base_user", "Base User"), ("hse_inspector", "HSE Inspector"),
                                           ("project_manager", "Project Manager"),
                                           ("company_representative", "Company Representative")),
                                  help_text="Select user type:")
    password = forms.CharField(validators=[validate_password], help_text="Password is generated automatically:")

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password'].initial = generate_password()
        self.fields['user_type'].choices = [choice for choice in self.fields['user_type'].choices
                                            if choice[0] != "company_representative"]


class EditUserForm(forms.Form):
    first_name = forms.CharField(min_length=1, max_length=35, help_text="Name of the user:")
    last_name = forms.CharField(min_length=1, max_length=50, help_text="Surname of the user")
    company = forms.CharField(min_length=1, max_length=50, help_text="Company of the user:")
    email = forms.EmailField(help_text="Email of the user:")
    password = forms.CharField(validators=[validate_password], required=False,
                               help_text="Leave empty, to not change password:")

    def __init__(self, *args, **kwargs):
        #  We need to catch argument that is passed to form, or we will have an error
        self.current_user = kwargs.pop('current_user', None)
        super(EditUserForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        # Allows to additionally affect email field with for example: validators
        email = self.cleaned_data.get('email')
        validate_unique_email(email, self.current_user)
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(validators=[validators.EmailValidator])
    password = forms.CharField(min_length=1, widget=forms.PasswordInput)


class ProjectDatabaseForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.none(), help_text="Select project database:")
    contractor = forms.CharField(min_length=1, max_length=60, help_text="Contractor name:")
    subcontractor = forms.CharField(max_length=60, help_text="Subcontractor name:")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), help_text="Select date:")
    average_number_people = forms.FloatField(min_value=0, help_text="Average number of people on site")
    hours_work = forms.IntegerField(min_value=0, help_text="Subcontractor total number of hours")

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(ProjectDatabaseForm, self).__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(user=self.current_user).order_by("name")


# Register form allow people to  fill the template which will be sent to customer companies email/or emails asking
# to be added.
class RegisterForm(forms.Form):
    company_tax_identification_number = forms.CharField(validators=[validate_companies_identification_number])
    first_name = forms.CharField(min_length=1, max_length=35)
    last_name = forms.CharField(min_length=1, max_length=50)
    company = forms.CharField(min_length=1, max_length=50)
    email = forms.EmailField(validators=[validators.EmailValidator, validate_unique_email])


class SiteObservationReportForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.none(), help_text="Select proejct:")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), help_text="Select date:")
    contractor = forms.CharField(max_length=60, help_text="Contractor name:")
    subcontractor = forms.CharField(max_length=60, help_text="Subcontractor name:")
    head_protection = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was head protection wore:")
    eyes_protection = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was eyes protection wore:")
    high_visible_clothes = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were high visible cloths wore:")
    foot_protection = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was correct foot protection boots wore:")
    hearing_protection = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was hearing protection wore:")
    respiratory_protection = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was respiratory protection wore:")
    hands_protection = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were hands protection equipment wore:")
    fall_arrest_equipment = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were fall arrest equipment wore:")
    general_work_permit = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was general work permit correct, in place, valid etc.:")
    hot_work_permit = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was hot work permit correct, in place, valid etc.::")
    confined_space_work_permit = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was confined space work permit correct, in place, valid etc.:")
    excavation_permit = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was excavation protection correct, etc.:")
    loto = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were rules regarding log out, tag out in place, etc.:")
    method_statement_and_risk_analysis = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were method statement or risk analysis correct, in place, valid, etc.:")
    lifting_permit_manual_handling = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was lifting permit manual handling on site:")
    routes_clear_of_obstructions = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were routes clear of obstructions:")
    housekeeping_standard_adequate = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were kept housekeeping standard adequate:")
    materials_stored_safely = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were materials stored safely:")
    correct_signage_posted = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were correct signage post used:")
    barrier_workplace = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was workplace barrier form rest of area:")
    dust_protection = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was dust protection equipment, rules used according to regulation:")
    waste_materials_segregated = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Where waste materials segregated correctly:")
    mobile_phone_used_ok = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was mobile phone used correctly, without increasing the risk of accident:")
    smoking_only_in_designated_areas = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Was workplace barrier form rest of area:")
    people_trained_for_site = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Does people on construction site after construction training, was the training still valid, etc.:")
    fire_extinguisher_and_water_bucket = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a",
        help_text="Were fire extinguisher or other form of fire protection present during hot works:")
    fire_watcher = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                     initial="n/a")
    flammable_materials_removed = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    gas_bottles_storage_and_usage = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    flame_arrestors_on_cylinders_and_torch = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    welding_screens = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                        initial="n/a")
    scaffolding_erected_and_used_according_the_manual = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    ladders_or_stepladders_secured_and_free_of_defects = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    personnel_trained_for_wah = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    fall_arrest_equipment_worn_and_used_correctly = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    safe_body_position = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                           initial="n/a")
    supervisor_for_wah_activities = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    authorized_personnel = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                             initial="n/a")
    lifting_coordinator_or_supervisor = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    no_people_under_suspended_load = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    lifting_gears_in_good_condition = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    tag_lines = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                  initial="n/a")
    shored_edges = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                     initial="n/a")
    walkways_and_bridges_over_excavations_have_guardrails_and_toe_boards = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    safe_and_enough_access = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                               initial="n/a")
    ladders_are_secured_and_extended_1_meter_above_the_edge_of_the_trench = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    spoils = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                               initial="n/a")
    materials_and_equipment_set_back_minimum_1_meter_from_the_edge_of_the_excavation = \
        forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                          initial="n/a")
    authorized_electrician = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                               initial="n/a")
    restricted_access_for_unauthorized_people = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    proper_insulated_tools_are_used = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    cabinets_are_closed_and_locked = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    specific_ppe_is_used = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                             initial="n/a")
    permit_to_work_posted_on_the_entrance = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    all_permit_to_work_requirements_are_in_place = \
        forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                          initial="n/a")
    only_authorized_personnel_for_confined_space_entry \
        = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                            initial="n/a")
    watchman_on_manhole = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                            initial="n/a")
    all_registers_are_updated = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    correct_tools = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                      initial="n/a")
    equipment_for_task = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                           initial="n/a")
    tools_and_equipment_used_correctly = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    tools_and_equipment_in_good_condition = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    operator_certified_for_equipment = forms.ChoiceField(
        choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
        initial="n/a")
    safe_guards_in_place = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                             initial="n/a")
    cables_leads = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                     initial="n/a")
    site_machinery = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                       initial="n/a")
    reverse_alarm = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                      initial="n/a")
    banksman = forms.ChoiceField(choices=(("n/a", "N/A"), ("present", "Present"), ("absent", "Absent")),
                                 initial="n/a")

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(SiteObservationReportForm, self).__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(user=self.current_user).order_by("name")
