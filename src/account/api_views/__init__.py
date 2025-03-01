from api.mixins import CreateListRetrieveViewSet

from api.rest import *

# from src.account.filters.staff_filters import StaffFilter
from src.account.models import StaffUser
from src.account.serializers import (
    EmployeeGradeSerializer,
    UserSerializer,
    StaffSerializer,
    DepartmentSerializer,
)
from src.account.staff import Department, EmployeeGrade, Staff
from utils.constants import DEFAULT_PERMS, DEFAULT_AUTH

# , DEFAULT_FILTER_BACKENDS


# Staff
class StaffListCreateAPIView(CreateListRetrieveViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    # filter_backends = DEFAULT_FILTER_BACKENDS
    # filter_class = StaffFilter
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
