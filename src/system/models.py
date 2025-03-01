from django.db import models

from src.account.staff import Staff
from utils.helpers import random_int_id


class Ownership(models.Model):
    owner_id = models.CharField(max_length=16, default=random_int_id(10))
    owner_name = models.CharField(max_length=30)
    desigination = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='media/system/ownership', null=True, blank=True)
    date_joined = models.DateField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.owner_name
    
    class Meta:
        verbose_name = "Ownership"
        verbose_name_plural = "Ownership"

class Organization(models.Model):
    organization_name = models.CharField(max_length=100)
    tag_line = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='media/system/logo', null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    mobile_number   = models.IntegerField(null=True, blank=True)
    tel_number  = models.IntegerField(null=True, blank=True)
    address     = models.TextField(max_length=255, null=True, blank=True)
    zip_code    = models.IntegerField(null=True, blank=True)
    working_hours = models.TextField(max_length=255, null=True, blank=True)
    capital = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    date_established = models.DateField(null=True, blank=True)
    ownership = models.ManyToManyField(Ownership)

    def __str__(self):
        return self.organization_name
    
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organization"
    
    def save(self, *args, **kwargs):
        org = Organization.objects.all()
        if org.exists():
            raise Exception("Organization already exists")
        return super().save(*args, **kwargs)

class SystemSettings(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.organization.organization_name

    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"

    @property
    def company_size(self):
        return str(Staff.objects.count())

    @property
    def owners(self):
        return self.ownership.all()
