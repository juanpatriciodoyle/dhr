from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import django
import datetime
from server import settings
# Create your models here.


class BaseModel(models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   editable=False, related_name="+", on_delete=models.PROTECT)

    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   editable=False, related_name="+", on_delete=models.PROTECT)

    created_at = models.DateTimeField(default=django.utils.timezone.now,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        abstract = True


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Employee(BaseModel):
    name = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)


class Address(BaseModel):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    postalCode = models.CharField(max_length=100)
    flat = models.CharField(max_length=100)


class HealthInsurance(BaseModel):
    number = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    expirationDate = models.DateField(auto_now=False)
    changeDate = models.DateField(auto_now=False)
    agreement = models.BooleanField(default=False)


class Bank(BaseModel):
    cbu = models.CharField(max_length=100)
    name = models.CharField(max_length=100)


class SocialNetworks(BaseModel):
    facebook = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)


class FamilyMember(BaseModel):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    relation = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    birthday = models.DateField(auto_now=False)


class WeeklySchedule(BaseModel):
    mondayFrom = models.DateField(auto_now=False)
    mondayTo = models.DateField(auto_now=False)
    tuesdayFrom = models.DateField(auto_now=False)
    tuesdayTo = models.DateField(auto_now=False)
    wednesdayFrom = models.DateField(auto_now=False)
    wednesdayTo = models.DateField(auto_now=False)
    thursdayFrom = models.DateField(auto_now=False)
    thursdayTo = models.DateField(auto_now=False)
    fridayFrom = models.DateField(auto_now=False)
    fridayTo = models.DateField(auto_now=False)
    satudayFrom = models.DateField(auto_now=False)
    saturdayTo = models.DateField(auto_now=False)


class WorkShift(BaseModel):
    weeklySchedule = models.ForeignKey()
    sectorType: Enum < SectorType >
