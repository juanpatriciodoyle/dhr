from datetime import datetime, timezone
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework.validators import UniqueValidator

from dhr.models import FamilyMember, WorkShift, Address, HealthInsurance, Bank, SocialNetworks, Docket, GenderType, \
    ContractType, Employee, WeeklySchedule, SectorType
from dhr.utils import get_default_admin_user

UserModel = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    read_only_fields = ('id', 'created_by', 'created_at', 'updated_by', 'updated_at',)

    class Meta:
        abstract = True

    def create(self, validated_data):

        user = self.context['request'].user
        if user.is_anonymous:
            user = get_default_admin_user()
        if 'request' in self.context:
            validated_data['created_by'] = user
            validated_data['updated_by'] = user

        return super(BaseSerializer, self).create(validated_data)

    def update(self, instance, validated_data):

        if 'request' in self.context:
            user = self.context['request'].user
            if user.is_anonymous:
                user = get_default_admin_user()
            validated_data['updated_by'] = user

        return super(BaseSerializer, self).update(instance, validated_data)


class CurrentUserSerializer(BaseSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=UserModel.objects.filter(is_active=True))])
    username = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=UserModel.objects.filter(is_active=True))])

    def create(self, validated_data):
        if UserModel.objects.filter(is_active=False, username=validated_data['username']).exists():
            UserModel.objects.filter(username=validated_data['username']).update(**validated_data, is_active=True)
            return UserModel.objects.get(username=validated_data['username'])

        user = UserModel.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = UserModel
        fields = ("id", "email", "username", "password", "first_name", "last_name")
        read_only_fields = ('id',)


class UsernameSerializer(BaseSerializer):
    class Meta:
        model = UserModel
        fields = ('username',)

        extra_kwargs = {
            'username': {'validators': []},
        }


class DocketSerializer(serializers.ModelSerializer):
    photo = serializers.CharField(max_length=100)
    docket_number = serializers.CharField(max_length=100)
    trial_period = serializers.BooleanField(default=False)
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    contract_type = serializers.ChoiceField(choices=[(contract, contract.value) for contract in ContractType])
    admission_date = serializers.DateField()
    egress_date = serializers.DateField()
    cuil = serializers.CharField(max_length=100)
    dni = serializers.CharField(max_length=100)
    birthday = serializers.DateField()
    phone1 = serializers.CharField(max_length=100)
    phone2 = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    gender_type = serializers.ChoiceField(choices=[(gender, gender.value) for gender in GenderType])
    holidays = serializers.CharField(max_length=100)
    environmental_policies = serializers.BooleanField(default=False)
    lambda_skills = serializers.BooleanField(default=False)
    back_office_metrics = serializers.BooleanField(default=False)
    work_shift_id = serializers.PrimaryKeyRelatedField(queryset=WorkShift.objects.all())
    address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    health_insurance_id = serializers.PrimaryKeyRelatedField(queryset=HealthInsurance.objects.all())
    bank_id = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all())
    social_networks_id = serializers.PrimaryKeyRelatedField(queryset=SocialNetworks.objects.all())
    family_member_id = serializers.PrimaryKeyRelatedField(queryset=FamilyMember.objects.all())
    deleted = serializers.BooleanField(default=False)

    class Meta:
        model = Docket
        fields = ("id", "photo", "docket_number", "trial_period", "name", "surname", "contract_type", "admission_date", "egress_date", "cuil", "dni", "birthday", "phone1", "phone2", "email", "gender_type", "holidays", "environmental_policies", "lambda_skills", "back_office_metrics", "work_shift_id", "address_id", "health_insurance_id", "bank_id", "social_networks_id", "family_member_id", "deleted")
        read_only_fields = ('id',)


class EmployeeSerializer(serializers.ModelSerializer):
    docket = serializers.PrimaryKeyRelatedField(queryset=Docket.objects.all())
    deleted = serializers.BooleanField(default=False)

    class Meta:
        model = Employee
        fields = ("id", "docket_id", "deleted")
        read_only_fields = ('id',)


class WorkShiftSerializer(serializers.ModelSerializer):
    weekly_schedule_id = serializers.PrimaryKeyRelatedField(queryset=WeeklySchedule.objects.all())
    sector_type = serializers.ChoiceField(choices=[(sector, sector.value) for sector in SectorType])

    class Meta:
        model = WorkShift
        fields = ("id", "weekly_schedule_id", "sector_type")
        read_only_fields = ('id',)


class WeeklyScheduleSerializer(serializers.ModelSerializer):
    monday_from = serializers.DateField()
    monday_to = serializers.DateField()
    tuesday_from = serializers.DateField()
    tuesday_to = serializers.DateField()
    wednesday_from = serializers.DateField()
    wednesday_to = serializers.DateField()
    thursday_from = serializers.DateField()
    thursday_to = serializers.DateField()
    friday_from = serializers.DateField()
    friday_to = serializers.DateField()
    saturday_from = serializers.DateField()
    saturday_to = serializers.DateField()

    class Meta:
        model = WeeklySchedule
        fields = ("id", "monday_from", "monday_to", "tuesday_from", "tuesday_to", "wednesday_from", "wednesday_to", "thursday_from", "thursday_to", "friday_from", "friday_to", "saturday_from", "saturday_to")
        read_only_fields = ('id',)


class FamilyMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    relation = serializers.CharField(max_length=100)
    dni = serializers.CharField(max_length=100)
    birthday = serializers.DateField()

    class Meta:
        model = FamilyMember
        fields = ("id", "name", "surname", "relation", "dni", "birthday")
        read_only_fields = ('id',)


class SocialNetworksSerializer(serializers.ModelSerializer):
    facebook = serializers.CharField(max_length=100)
    instagram = serializers.CharField(max_length=100)

    class Meta:
        model = SocialNetworks
        fields = ("id", "facebook", "instagram")
        read_only_fields = ('id',)


class BankSerializer(serializers.ModelSerializer):
    cbu = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Bank
        fields = ("id", "cbu", "name")
        read_only_fields = ('id',)


class HealthInsuranceSerializer(serializers.ModelSerializer):
    number = serializers.CharField(max_length=100)
    company = serializers.CharField(max_length=100)
    expirationDate = serializers.DateField()
    changeDate = serializers.DateField()
    agreement = serializers.BooleanField(default=False)

    class Meta:
        model = HealthInsurance
        fields = ("id", "number", "company", "expirationDate", "changeDate", "agreement")
        read_only_fields = ('id',)


class AddressSerializer(serializers.ModelSerializer):
    street = serializers.CharField(max_length=100)
    number = serializers.CharField(max_length=100)
    postalCode = serializers.CharField(max_length=100)
    flat = serializers.CharField(max_length=100)

    class Meta:
        model = Address
        fields = ("id", "street", "number", "postalCode", "flat")
        read_only_fields = ('id',)
