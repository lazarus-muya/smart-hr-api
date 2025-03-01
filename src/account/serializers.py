from datetime import datetime as dt
from rest_framework import serializers

from src.administration.serializers import (
    AttendanceSerializer,
    LeaveRequestSerializer,
    StaffTrainingSerializer,
)
from src.directory.serializers import DocumentSerializer
from src.finance.serializers import BankSerializer, PayrollRecordSerializer

from .staff import EmployeeGrade, Staff, Department, HeadOfDepartment
from .models import StaffUser

from .staff import WorkPlace


class HodSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadOfDepartment
        fields = "__all__"


class EmployeeGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeGrade
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class UserResetPasswordSerializer(serializers.Serializer):
    # otp = serializers.CharField(default=random_int_id(6), label="OTP", help_text="OTP")
    email = serializers.EmailField(required=True)

    class Meta:
        model = StaffUser
        fields = ("email",)


class StaffSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()
    trainings = serializers.SerializerMethodField()
    payroll = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()
    leaves = serializers.SerializerMethodField()
    hod = serializers.SerializerMethodField()
    department = DepartmentSerializer(read_only=True)
    grade = EmployeeGradeSerializer(read_only=True)
    bank = BankSerializer(read_only=True)
    leaves = LeaveRequestSerializer(
        many=True, read_only=True, source="leaverequest_set"
    )
    date_of_birth = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = "__all__"

    def validate(self, attr):
        request = self.context["request"]
        staff_id = attr["staff_id"]
        staff = Staff.objects.filter(staff_id=staff_id).exists()
        if staff and request.method and request.method == "POST":
            raise serializers.ValidationError(
                detail="Staff with this details already exists.", code=409
            )
        return attr

    def get_documents(self, obj):
        _serializer = DocumentSerializer(obj.staff_documents, many=True)
        return _serializer.data

    def get_trainings(self, obj):
        _training = StaffTrainingSerializer(obj.list_trainings, many=True)
        return _training.data

    def get_hod(self, obj):
        if not obj.reporting_to:
            return None
        _staff = obj.reporting_to
        hodData = {
            "staff_id": _staff.staff_id,
            "name": f"{_staff.first_name} {_staff.last_name}",
            "email": _staff.email,
            "phone_number": _staff.phone_number,
            "department": DepartmentSerializer(_staff.department).data,
        }
        return hodData

    def get_payroll(self, obj):
        return PayrollRecordSerializer(obj.staff_payroll, many=True).data

    def get_leaves(self, obj):
        return LeaveRequestSerializer(obj.staff_leaves, many=True).data

    def get_attendance(self, obj):
        return AttendanceSerializer(obj.attendance, many=True).data
    
    def get_date_of_birth(self, obj):
        if type(obj.date_of_birth) == dt:
            return obj.date_of_birth.date()
        return obj.date_of_birth


class WorkPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlace
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True, required=False)

    class Meta:
        model = StaffUser
        fields = (
            "staff_id",
            "staff",
            "last_login",
            "is_superuser",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "is_staff",
            "is_active",
            "phone_number",
        )
        depth = 1
