from djangorestframework_camel_case.parser import CamelCaseJSONParser, CamelCaseMultiPartParser, CamelCaseFormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from src.account.serializers import StaffSerializer, BankSerializer, WorkplaceSerializer, DepartmentSerializer, EmployeeGradeSerializer
from src.account.staff import Staff, WorkPlace, Bank, Department, EmployeeGrade
from utils.constants import DEFAULT_PERMS, DEFAULT_AUTH, DEBUG_AUTH, DEBUG_PERMS

from api.mixins import CreateListRetrieveViewSet

from api.rest import *


from src.account.models import StaffUser
from src.account.serializers import (
    EmployeeGradeSerializer,
    UserSerializer,
    StaffSerializer,
    DepartmentSerializer,
    WorkplaceSerializer,
)
from src.account.staff import Department, EmployeeGrade, Staff, WorkPlace
from utils.constants import DEFAULT_PERMS, DEFAULT_AUTH


class StaffApiView(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    authentication_classes = DEBUG_AUTH
    permission_classes = DEBUG_PERMS
    # pagination_class = PageNumberPagination
    parser_classes = [CamelCaseJSONParser, CamelCaseMultiPartParser, CamelCaseFormParser, FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        data = request.data
        for field in ['workplace', 'department', 'grade', 'bank']:
            if field in data and data[field] is not None:
                data[field] = int(data[field])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)  # Validate data
        self.perform_create(serializer)  # Save instance

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Apply filters if needed
        # page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(queryset, many=True)
        for obj in serializer.data:
            if obj['workplace'] is not None:
                wp = WorkPlace.objects.get(pk=obj['workplace'])
                obj['workplace'] = WorkplaceSerializer(wp).data
            if obj['department'] is not None:
                dp = Department.objects.get(pk=obj['department'])
                obj['department'] = DepartmentSerializer(dp).data
            if obj['grade'] is not None:
                eg = EmployeeGrade.objects.get(pk=obj['grade'])
                obj['grade'] = EmployeeGradeSerializer(eg).data
            if obj['bank'] is not None:
                bank = Bank.objects.get(pk=obj['bank'])
                obj['bank'] = BankSerializer(bank).data
        # if page is not None:
            # serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        return self.__update_data(data, is_partial=True)

    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()
        return self.__update_data(data, is_partial=True)
    
    def __update_data(self, data, is_partial=False):
        instance = self.get_object()        
        for field in ['workplace', 'department', 'grade', 'bank']:
            if field in data and data[field] is not None:
                data[field] = int(data[field])

        serializer = self.get_serializer(instance, data=data, partial=is_partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

# Workplace
class WorkplaceListCreateAPIView(CreateListRetrieveViewSet):
    queryset = WorkPlace.objects.all()
    serializer_class = WorkplaceSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS


# Departments
class DepartmentListCreateAPIView(CreateListRetrieveViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS


# EmployeeGrade
class GradeRetrieveUpdateDestroyAPIView(CreateListRetrieveViewSet):
    queryset = EmployeeGrade.objects.all()
    serializer_class = EmployeeGradeSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS


# Users
class UserListCreateAPIView(CreateListRetrieveViewSet):
    queryset = StaffUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS
