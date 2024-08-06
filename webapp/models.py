from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


# Create your models here.
# Emails connected to CustomerCompany model, which will be selected as designated email during registration.
class CustomerCompanyEmails(models.Model):
    email = models.EmailField()

    def __str__(self):
        return f"{self.email}"


class CustomerCompany(models.Model):
    name = models.CharField(max_length=75)
    taxpayer_identification_number = models.IntegerField(unique=True)
    num_of_projects = models.IntegerField()
    general_emails = models.ManyToManyField(CustomerCompanyEmails)

    def __str__(self):
        return f"{self.name}"


# It's my CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email, )
        user = self.model(username=username.strip(), email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=40, choices=(("base_user", "Base User"),
                                                         ("hse_inspector", "HSE Inspector"),
                                                         ("project_manager", "Project Manager"),
                                                         ("company_representative", "Company Representative")))
    user_company = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Project(models.Model):
    name = models.CharField(max_length=30)
    company = models.ForeignKey(CustomerCompany, on_delete=models.CASCADE)
    user = models.ManyToManyField(CustomUser, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.company}-{self.name}")
        super().save(*args, **kwargs)


class ProjectDatabase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contractor = models.CharField(max_length=60)
    subcontractor = models.CharField(max_length=60)
    date = models.DateField()
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.CharField(max_length=20)
    average_number_people = models.FloatField()
    hours_work = models.IntegerField()


class CardAndIncident(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contractor = models.CharField(max_length=60)
    subcontractor = models.CharField(max_length=60)
    name_surname = models.CharField(max_length=80)
    date = models.DateField()
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.CharField(max_length=20)
    type = models.CharField(max_length=40, choices=(
        ("alcohol", "Alcohol"),
        ("hazard_situation", "Hazard Situation"),
        ("near_miss", "Near Miss"),
        ("positive_observation", "Positive Observation")
    ))
    description = models.CharField(max_length=100)
    issued_card = models.CharField(max_length=40, choices=(
        ("green", "Green"),
        ("yellow", "Yellow"),
        ("red", "Red"),
        ("black", "Black")
    ))

    def __str__(self):
        return f"{self.project}-{self.contractor}-{self.issued_card}"


class SiteObservationReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.CharField(max_length=20)
    sor_observer = models.CharField(max_length=60)
    observer_company = models.CharField(max_length=60)
    contractor = models.CharField(max_length=60)
    subcontractor = models.CharField(max_length=60)
    head_protection = models.CharField(max_length=60,
                                       choices=(("present", "Present"),
                                                ("absent", "Absent")))
    eyes_protection = models.CharField(max_length=60,
                                       choices=(("present", "Present"),
                                                ("absent", "Absent")))
    high_visible_clothes = models.CharField(max_length=60,
                                            choices=(("present", "Present"),
                                                     ("absent", "Absent")))
    foot_protection = models.CharField(max_length=60,
                                       choices=(("present", "Present"),
                                                ("absent", "Absent")))
    hearing_protection = models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    respiratory_protection = models.CharField(max_length=60, blank=True, null=True,
                                              choices=(("present", "Present"),
                                                       ("absent", "Absent")))
    hands_protection = models.CharField(max_length=60, blank=True, null=True,
                                        choices=(("present", "Present"),
                                                 ("absent", "Absent")))
    fall_arrest_equipment = models.CharField(max_length=60, blank=True, null=True,
                                             choices=(("present", "Present"),
                                                      ("absent", "Absent")))
    general_work_permit = models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    hot_work_permit = models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    confined_space_work_permit =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    excavation_permit =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    loto =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    method_statement_and_risk_analysis =  models.CharField(max_length=60, blank=True, null=True,
                                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    lifting_permit_manual_handling =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    routes_clear_of_obstructions =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    housekeeping_standard_adequate =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    materials_stored_safely =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    correct_signage_posted  =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    barrier_workplace =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    dust_protection =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    waste_materials_segregated =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    mobile_phone_used_ok =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    smoking_only_in_designated_areas =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    people_trained_for_site =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    fire_extinguisher_and_water_bucket =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    fire_watcher =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    flammable_materials_removed =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    gas_bottles_storage_and_usage =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    flame_arrestors_on_cylinders_and_torch =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    welding_screens =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    scaffolding_erected_and_used_according_the_manual =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    ladders_or_stepladders_secured_and_free_of_defects =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    personnel_trained_for_wah =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    fall_arrest_equipment_worn_and_used_correctly =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    safe_body_position =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    supervisor_for_wah_activities =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    authorized_personnel =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    lifting_coordinator_or_supervisor =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    no_people_under_suspended_load =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    lifting_gears_in_good_condition =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    tag_lines =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    shored_edges =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    walkways_and_bridges_over_excavations_have_guardrails_and_toe_boards =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    safe_and_enough_access =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    ladders_are_secured_and_extended_1_meter_above_the_edge_of_the_trench =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    spoils =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    materials_and_equipment_set_back_minimum_1_meter_from_the_edge_of_the_excavation =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    authorized_electrician =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    restricted_access_for_unauthorized_people =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    proper_insulated_tools_are_used =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    cabinets_are_closed_and_locked =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    specific_ppe_is_used =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    permit_to_work_posted_on_the_entrance =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    all_permit_to_work_requirements_are_in_place =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    only_authorized_personnel_for_confined_space_entry =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    watchman_on_manhole =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    all_registers_are_updated =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    correct_tools =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    equipment_for_task =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    tools_and_equipment_used_correctly =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    tools_and_equipment_in_good_condition =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    operator_certified_for_equipment =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    safe_guards_in_place =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    cables_leads =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    site_machinery =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    reverse_alarm =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
    banksman =  models.CharField(max_length=60, blank=True, null=True,
                                          choices=(("present", "Present"),
                                                   ("absent", "Absent")))
