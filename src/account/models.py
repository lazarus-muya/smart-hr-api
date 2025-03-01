from django.contrib.auth.models import AbstractUser
from django.db import models

from src.hrm import *
from .staff import Staff
from .manager import StaffUserManager


class StaffUser(AbstractUser):
    username    = None
    staff       = models.OneToOneField(Staff, on_delete=models.CASCADE, null=True, blank=True)
    email       = models.EmailField(unique=True)
    phone_number = models.IntegerField(unique=True)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    metadata    = models.JSONField(null=True, blank=True, default=dict)
    objects = StaffUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    @property
    def full_name(self):
        return self.staff.full_name

    @property
    def profile_picture(self):
        if not self.staff:
            return None
        if not self.staff.profile_picture:
            return None
        return self.staff.profile_picture

    def __str__(self):
        return self.full_name if self.staff else str(self.phone_number)
