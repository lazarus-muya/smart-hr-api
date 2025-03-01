from django.db import models

from src.hrm import *
from src.finance.bank import Bank
from utils.options import EducationLevels
from utils.validators import TitleCaseField


class Department(models.Model):
    department_name = TitleCaseField(max_length=255)

    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
    
    def hod(self):
        return self.hoddepartment.first()


class WorkPlace(models.Model):
    workplace_name = TitleCaseField(max_length=255)
    address         = models.TextField(null=True, blank=True)
    openning_time   = models.TimeField(null=True, blank=True)
    clossing_time   = models.TimeField(null=True, blank=True)
    open_on_weekends = models.BooleanField(default=False)

    def __str__(self):
        return self.work_place_name

    class Meta:
        verbose_name        = "Work Location"
        verbose_name_plural = "Work Locations"

class EmployeeGrade(models.Model):
    grade = TitleCaseField(max_length=30)
         
    def __str__(self):
        return self.grade

    class Meta:
        verbose_name        = "Employee Grade"
        verbose_name_plural = "Employee Grades"

class  Staff(models.Model):
    staff_id        = TitleCaseField(max_length=16, default=timestamp_id(16), unique=True, primary_key=True)
    first_name      = TitleCaseField(max_length=255)
    middle_name     = TitleCaseField(max_length=255, null=True, blank=True)
    last_name       = TitleCaseField(max_length=255)
    email           = models.EmailField(unique=True)
    phone_number    = models.CharField(max_length=20, unique=True)
    date_of_birth   = models.DateField()
    gender          = TitleCaseField(max_length=14, default=GenderChoices.DEFAULT, choices=GenderChoices.choices)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="staffs/profile/")
    id_number       = models.BigIntegerField(null=True, blank=True, unique=True)
    address         = models.TextField(null=True, blank=True)
    joining_date    =  models.DateField(default=timezone.now)
    acccess_card    = TitleCaseField(max_length=12, null=True, blank=True, unique=True)
    account_number  = models.BigIntegerField(null=True, blank=True, unique=True)
    education_level = TitleCaseField(max_length=14, choices=EducationLevels.choices, default=EducationLevels.DEFAULT)
    status          = models.CharField(max_length=20, choices=StaffStatus.choices, default=StaffStatus.ACTIVE)
    skills          = models.TextField(null=True, blank=True)
    bank            = models.ForeignKey(Bank, db_column="staff_bank_name", on_delete=models.SET_NULL, null=True, blank=True,)
    work_place      = models.ForeignKey(WorkPlace, on_delete=models.SET_NULL, null=True, blank=True)
    grade           = models.ForeignKey(EmployeeGrade, on_delete=models.SET_NULL, null=True, blank=True)
    department      = models.ForeignKey(Department, related_name="staffdepartment", on_delete=models.SET_NULL, null=True, blank=True)
    medical_card_number = TitleCaseField(max_length=12, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["phone_number"], name="staff_phone_number_idx"),
            models.Index(fields=["id_number"], name="staff_id_number_idx"),
            models.Index(fields=["staff_id"], name="staff_staff_id_idx"),
            models.Index(fields=["email"], name="staff_staff_email_idx"),
        ]
        ordering = ["-joining_date"]
        verbose_name        = "Staff"
        verbose_name_plural = "Staffs"

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return "staffs/{}".format(self.staff_id)

    @property
    def staff_documents(self):
        return self.document_set.all()

    @property
    def tax(self):
        return self.taxinformation_set.all()

    @property
    def list_trainings(self):
        return self.trainingprogram_set.all()

    def __str__(self):
        return self.full_name

    @property
    def reporting_to(self):
        if not self.department:
            return
        _department = Department.objects.get(
            department_name = self.department.department_name
        )
        _hod = HeadOfDepartment.objects.filter(department=_department)
        if _hod.exists():
            return _hod.first().hod
        return None

    @property
    def staff_payroll(self):
        return self.payrollrecord_set.all()

    @property
    def attendance(self):
        # return self.attendance_set.all()
        return self.staff_name.all()

    @property
    def staff_leaves(self):
        return self.leaverequest_set.all()

class HeadOfDepartment(models.Model):
    hod         = models.ForeignKey(Staff, related_name="hodstaff", on_delete=models.CASCADE)
    department  = models.ForeignKey(Department, related_name="hoddepartment", on_delete=models.CASCADE)

    def __str__(self):
        return self.hod.full_name

    class Meta:
        verbose_name = "Head of Department"
        verbose_name_plural = "Heads of Departments"


 