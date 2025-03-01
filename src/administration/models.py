from datetime import datetime as dt

from django.db import models
from django.utils import timezone

from src.account.staff import HeadOfDepartment, Staff
from utils.options import (LeaveType, LeaveStatus)


class Attendance(models.Model):
    staff   = models.ForeignKey(Staff, related_name='staff_name', on_delete=models.CASCADE)
    date    = models.DateField(default=timezone.now)
    clock_in_time   = models.TimeField(default=timezone.now)
    clock_out_time  = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.staff.full_name

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"

    @property
    def hours_worked(self):
        
        if not self.clock_out_time:
            return 0
        # if self.clock_out_time is None:
        #     return timezone.now().time - self.clock_in_time
        time_worked = dt.combine(
            dt.today(), self.clock_out_time) - dt.combine(dt.today(), self.clock_in_time)
        return "%.2f hours" % float(time_worked.seconds.real / 3600)


class LeaveRequest(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_type = models.CharField(
        max_length=20, default=LeaveType.ANNUAL, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, default=LeaveStatus.PENDING, choices=LeaveStatus.choices)

    def __str__(self):
        return self.staff

    class Meta:
        verbose_name = "Leave Request"
        verbose_name_plural = "Leave Requests"


class TrainingProgram(models.Model):
    program_name    = models.CharField(max_length=255)
    description     = models.TextField(null=True, blank=True)
    trainer        = models.CharField(max_length=30, null=True, blank=True)
    duration        = models.CharField(max_length=30, null=True, blank=True)
    start_date      = models.DateField()
    end_date        = models.DateField()
    staffs          = models.ManyToManyField(Staff)
    # Added duration and trainer field

    def __str__(self):
        return self.program_name

    class Meta:
        verbose_name = "Training Program"
        verbose_name_plural = "Training Programs"


class PerformanceReview(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    review_date = models.DateField()
    hod = models.ForeignKey(
        HeadOfDepartment, related_name='reviewer', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):  
        return self.staff

    class Meta:
        verbose_name = "Performance Review"
        verbose_name_plural = "Performance Reviews"
