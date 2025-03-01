from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import StaffUserChangeForm, StaffUserCreationForm, StaffUser
from .staff import Staff, Department, HeadOfDepartment, EmployeeGrade
from src.account.staff import WorkPlace


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "staff_id",
        "full_name",
        "email",
        "phone_number",
        "department",
        "joining_date",
    )
    # readonly_fields = ("staff_id",)

    def full_name(self, obj):
        return obj.full_name


@admin.register(StaffUser)
class StaffUserAdmin(UserAdmin):
    add_form = StaffUserCreationForm
    form = StaffUserChangeForm
    model = StaffUser
    list_display = ("staff_id", "staff", "email", "phone_number", "role")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("phone_number",)
    ordering = ("phone_number",)

    def user_id(self, obj):
        return obj.staff.staff_id

    def full_name(self, obj):
        return obj.staff.full_name

    def department(self, obj):
        return obj.staff.department

    def role(self, obj):
        if obj.is_superuser:
            return "Admin"
        return "Staff"

    fieldsets = (
        ("Personal Details", {"fields": ("phone_number", "email", "staff")}),
        (
            "Permisions",
            {
                "classes": ["collapse"],
                "fields": ("is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("department_name",)


@admin.register(HeadOfDepartment)
class HeadOfDepartmentAdmin(admin.ModelAdmin):
    list_display = ("hod", "department")


@admin.register(EmployeeGrade)
class EmployeeGradeAdmin(admin.ModelAdmin):
    list_display = ("grade",)


@admin.register(WorkPlace)
class WorkPlaceAdmin(admin.ModelAdmin):
    list_display = ("workplace_name", "address", "openning_time", "clossing_time")
