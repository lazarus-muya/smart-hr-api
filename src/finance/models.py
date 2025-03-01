from django.db import models

from src.account.staff import Staff
from utils.options import (
    AllowanceChoices, MonthsOptions, SalaryTypes, PaymentMethods)
from utils.validators import *


class TaxInformation(models.Model):
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, null=True, blank=True)
    tax_bracket = models.CharField(max_length=255)
    exemptions = models.IntegerField()
    deductions = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Tax Information"
        verbose_name_plural = "Tax Informations"

    def __str__(self):
        return self.staff.full_name


class Benefit(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    benefit_name = models.CharField(max_length=255)
    benefit_type = models.CharField(max_length=255)
    contribution_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # TODO: change contribution_amount to amount

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"

    def __str__(self):
        return self.staff.full_name


class Allowance(models.Model):
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name='staff_allowance')
    month = models.CharField(max_length=20, choices=MonthsOptions.choices)
    allowance = models.CharField(
        max_length=50, default=AllowanceChoices.DEFAULT, choices=AllowanceChoices.choices)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['month']
        verbose_name = "Allowance"
        verbose_name_plural = "Allowances"

    def __str__(self):
        return self.staff.full_name


class Deduction(models.Model):
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name='deducted_staff')
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    date_deducted = models.DateField(null=True, blank=True)
    reason = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['date_deducted']
        verbose_name = "Deduction"
        verbose_name_plural = "Deductions"

    def __str__(self):
        return self.staff.full_name


class PayrollRecord(models.Model):
    staff = models.ForeignKey("account.Staff", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()  # validators=[validate_end_date, ]
    month = models.CharField(max_length=20, choices=MonthsOptions.choices)
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.ManyToManyField(Allowance)
    deductions = models.ManyToManyField(Deduction)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    salary_type = models.CharField(
        max_length=20, choices=SalaryTypes.choices, default=SalaryTypes.MONTHLY)
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethods.choices, default=PaymentMethods.BANK)

    # TODO: Add Overtime Rate, Pay Date, Overtime Hours
    # TODO: remove salary_type
    # TODO: change basic_pay to basic_salary

    class Meta:
        ordering = ['-start_date', '-month']
        get_latest_by = ['-start_date']
        verbose_name = "Payroll Record"
        verbose_name_plural = "Payroll Records"

    @property
    def net_pay(self):
        allowances = sum([i.amount for i in self.allowances.prefetch_related("allowances").all()])
        deductions = sum([i.amount for i in self.deductions.prefetch_related("deductions").all()])
        return (float(self.basic_pay) + float(self.bonus) + float(allowances)) - float(deductions)

    def __str__(self):
        return self.staff.full_name


class SalaryStructure(models.Model):
    structure_name = models.CharField(max_length=255)
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['structure_name']
        verbose_name = "Salary Structure"
        verbose_name_plural = "Salary Structures"

    def __str__(self):
        return self.structure_name


class SalaryComponent(models.Model):
    component_name = models.CharField(max_length=255)
    component_type = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE)

    class Meta:
        ordering = ['component_name']
        verbose_name = "Salary Component"
        verbose_name_plural = "Salary Components"

    def __str__(self):
        return self.component_name


