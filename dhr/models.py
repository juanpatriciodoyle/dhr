from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import django
from enum import Enum
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


class Address(BaseModel):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    postalCode = models.CharField(max_length=100)
    flat = models.CharField(max_length=100)


class HealthInsurance(BaseModel):
    number = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    expirationDate = models.DateField()
    changeDate = models.DateField()
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
    birthday = models.DateField()


class WeeklySchedule(BaseModel):
    monday_from = models.DateField()
    monday_to = models.DateField()
    tuesday_from = models.DateField()
    tuesday_to = models.DateField()
    wednesday_from = models.DateField()
    wednesday_to = models.DateField()
    thursday_from = models.DateField()
    thursday_to = models.DateField()
    friday_from = models.DateField()
    friday_to = models.DateField()
    saturday_from = models.DateField()
    saturday_to = models.DateField()


class SectorType(Enum):
    MANAGER = "MANAGER"
    BACK_OFFICE_MANAGER = "BACK_OFFICE_MANAGER"
    TRAINER = "TRAINER"
    QUALITY_MANGER = "QUALITY_MANGER"
    ACCOUNT_MANAGER = "ACCOUNT_MANAGER"
    SYSTEMS_ANALYST = "SYSTEMS_ANALYST"
    REAL_TIME_MANAGER = "REAL_TIME_MANAGER"
    ADMINISTRATIVE_ASSISTANT = "ADMINISTRATIVE_ASSISTANT"
    HR_ANALYST = "HR_ANALYST"
    ACCOUNTANT = "ACCOUNTANT"
    MANAGEMENT = "MANAGEMENT"
    PRESIDENT = "PRESIDENT"


class WorkShift(BaseModel):
    weekly_schedule = models.ForeignKey(WeeklySchedule, on_delete=models.CASCADE)
    sector_type = models.CharField(max_length=25, choices=[(sector, sector.value) for sector in SectorType])


class ContractType(Enum):
    TRIAL = "TRIAL"
    INDETERMINATE = "INDETERMINATE"
    DETERMINE = "DETERMINE"


class GenderType(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class Docket(BaseModel):
    photo = models.CharField(max_length=100)
    docket_number = models.CharField(max_length=100)
    trial_period = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    contract_type = models.CharField(max_length=25, choices=[(contract, contract.value) for contract in ContractType])
    admission_date = models.DateField()
    egress_date = models.DateField()
    cuil = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    birthday = models.DateField()
    phone1 = models.CharField(max_length=100)
    phone2 = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    gender_type = models.CharField(max_length=10, choices=[(gender, gender.value) for gender in GenderType])
    holidays = models.CharField(max_length=100)
    environmental_policies = models.BooleanField(default=False)
    lambda_skills = models.BooleanField(default=False)
    back_office_metrics = models.BooleanField(default=False)
    work_shift = models.ForeignKey(WorkShift, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    health_insurance = models.ForeignKey(HealthInsurance, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    social_networks = models.ForeignKey(SocialNetworks, on_delete=models.CASCADE)
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)


class Employee(BaseModel):
    docket = models.ForeignKey(Docket, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)


class User(AbstractUser):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    deleted = models.BooleanField(default=False)
