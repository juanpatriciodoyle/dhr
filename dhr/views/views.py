import django_filters

from django.contrib.auth import get_user_model
from django_filters import FilterSet

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from dhr.models import Employee, Docket, WorkShift, WeeklySchedule, FamilyMember, SocialNetworks, Bank, HealthInsurance, \
    Address
from dhr.serializers import UserSerializer, DocketSerializer, EmployeeSerializer, WorkShiftSerializer, \
    WeeklyScheduleSerializer, FamilyMemberSerializer, SocialNetworksSerializer, BankSerializer, \
    HealthInsuranceSerializer, AddressSerializer
from dhr.utils import CustomPageNumberPagination
from django.http import Http404


User = get_user_model()


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name'
        )


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().filter(is_active=1, is_superuser=0)
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('first_name', 'last_name')
    filter_class = UserFilter

    def destroy(self, request, pk=None, **kwargs):
        try:
            user = self.get_object()
            user.is_active = False
            user.save()
        except Http404:
            return Response("User does not exist", 404)

        return Response("User deleted", 204)


class DocketView(viewsets.ModelViewSet):
    serializer_class = DocketSerializer
    queryset = Docket.objects.all().filter(deleted=0)
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('cuil', 'dni', 'name', 'surname', 'docketNumber')

    def destroy(self, request, pk=None, **kwargs):
        try:
            docket = self.get_object()
            docket.deleted = True
            docket.save()
        except Http404:
            return Response("Docket does not exist", 404)

        return Response("Docket deleted", 204)


class EmployeeView(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all().filter(deleted=0)
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('',)
    # TODO Search_fields by docket.employee_name?

    def destroy(self, request, pk=None, **kwargs):
        try:
            employee = self.get_object()
            employee.deleted = True
            employee.save()
        except Http404:
            return Response("Employee does not exist", 404)

        return Response("Employee deleted", 204)


class WorkShiftView(viewsets.ModelViewSet):
    serializer_class = WorkShiftSerializer
    queryset = WorkShift.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('',)
    # TODO No Search_fields

    def destroy(self, request, pk=None, **kwargs):
        try:
            workShift = self.get_object()
            workShift.deleted = True
            workShift.save()
        except Http404:
            return Response("Work Shift does not exist", 404)

        return Response("Work Shift deleted", 204)


class WeeklyScheduleView(viewsets.ModelViewSet):
    serializer_class = WeeklyScheduleSerializer
    queryset = WeeklySchedule.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('',)
    # TODO No Search_fields

    def destroy(self, request, pk=None, **kwargs):
        try:
            weeklySchedule = self.get_object()
            weeklySchedule.deleted = True
            weeklySchedule.save()
        except Http404:
            return Response("Weekly Schedule does not exist", 404)

        return Response("Weekly Schedule deleted", 204)


class FamilyMemberView(viewsets.ModelViewSet):
    serializer_class = FamilyMemberSerializer
    queryset = FamilyMember.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('',)
    # TODO No Search_fields

    def destroy(self, request, pk=None, **kwargs):
        try:
            familyMember = self.get_object()
            familyMember.deleted = True
            familyMember.save()
        except Http404:
            return Response("Family Member does not exist", 404)

        return Response("Family Member deleted", 204)


class SocialNetworksView(viewsets.ModelViewSet):
    serializer_class = SocialNetworksSerializer
    queryset = SocialNetworks.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('',)
    # TODO No Search_fields

    def destroy(self, request, pk=None, **kwargs):
        try:
            socialNetworks = self.get_object()
            socialNetworks.deleted = True
            socialNetworks.save()
        except Http404:
            return Response("Social Networks does not exist", 404)

        return Response("Social Networks deleted", 204)


class BankView(viewsets.ModelViewSet):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('cbu',)

    def destroy(self, request, pk=None, **kwargs):
        try:
            bank = self.get_object()
            bank.deleted = True
            bank.save()
        except Http404:
            return Response("Bank does not exist", 404)

        return Response("Bank deleted", 204)


class HealthInsuranceView(viewsets.ModelViewSet):
    serializer_class = HealthInsuranceSerializer
    queryset = HealthInsurance.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('number', 'company')

    def destroy(self, request, pk=None, **kwargs):
        try:
            healthInsurance = self.get_object()
            healthInsurance.deleted = True
            healthInsurance.save()
        except Http404:
            return Response("Health Insurance does not exist", 404)

        return Response("Health Insurance deleted", 204)


class AddressView(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ('street', 'number', 'postalCode')

    def destroy(self, request, pk=None, **kwargs):
        try:
            address = self.get_object()
            address.deleted = True
            address.save()
        except Http404:
            return Response("Address does not exist", 404)

        return Response("Address deleted", 204)
