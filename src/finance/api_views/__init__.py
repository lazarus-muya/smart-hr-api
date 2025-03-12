from rest_framework.response import Response


from api.rest import *
from src.finance.models import Allowance, Deduction
from src.finance.bank import Bank
from src.finance.serializers import (
    AllowanceSerializer,
    BenefitSerializer,
    DeductionSerializer,
    PayrollRecordSerializer,
    SalaryComponentSerializer,
    SalaryStructureSerializer,
    TaxInformationSerializer,
    BankSerializer
)
from utils.constants import DEFAULT_AUTH, DEFAULT_PERMS


# Bank
class BankListCreateAPIView(CreateListRetrieveViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS


# Salary


class SalaryStructureListCreateAPIView(CreateListRetrieveViewSet):
    queryset = SalaryStructure.objects.all()
    serializer_class = SalaryStructureSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS


class SalaryComponentListCreateAPIView(CreateListRetrieveViewSet):
    queryset = SalaryComponent.objects.all()
    serializer_class = SalaryComponentSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS


class AllowanceApiView(StaffListRetrieveMixin):
    queryset = Allowance.objects.all()
    serializer_class = AllowanceSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS


class DeductionApiView(StaffListRetrieveMixin):
    queryset = Deduction.objects.all()
    serializer_class = DeductionSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS


# Payroll
class PayrollRecordListCreateAPIView(StaffListRetrieveMixin):
    queryset = PayrollRecord.objects.all()
    serializer_class = PayrollRecordSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS

    def create(self, request, *args, **kwargs):
        data = request.data
        _allowances = [Allowance.objects.get(pk=pk) for pk in data["allowances"]]
        _deductions = [Deduction.objects.get(pk=pk) for pk in data["deductions"]]

        record = PayrollRecord.objects.create(
            start_date=data["start_date"],
            end_date=data["end_date"],
            month=data["month"],
            basic_pay=data["basic_pay"],
            bonus=data["bonus"],
            staff=Staff.objects.get(staff_id=data["staff"]),
        )
        record.allowances.set(_allowances)
        record.deductions.set(_deductions)
        _serializer = PayrollRecordSerializer(record)
        return Response(_serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        data = request.data
        record = PayrollRecord.objects.create(
            start_date=data["start_date"],
            end_date=data["end_date"],
            month=data["month"],
            basic_pay=data["basic_pay"],
            bonus=data["bonus"],
            staff=Staff.objects.get(staff_id=data["staff"]),
        )
        record.allowances.set(data["allowances"])
        record.deductions.set(data["deductions"])
        _serializer = PayrollRecordSerializer(record)
        return Response(_serializer.data, status=200)


# Tax
class TaxInformationListCreateAPIView(CreateListRetrieveViewSet):
    queryset = TaxInformation.objects.all()
    serializer_class = TaxInformationSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS

    def create(self, request, *args, **kwargs):
        data = request.data
        tax = TaxInformation.objects.create(
            staff=Staff.objects.get(staff_id=data["staff"]["staff_id"]),
            deductions=data["deductions"],
            exemptions=data["exemptions"],
            tax_bracket=data["tax_bracket"],
        )
        _serializer = TaxInformationSerializer(tax)
        return Response(_serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        data = request.data
        tax = TaxInformation.objects.update(
            staff=data["staff"],
            deductions=data["deductions"],
            exemptions=data["exemptions"],
            tax_bracket=data["tax_bracket"],
        )
        _serializer = TaxInformationSerializer(data=tax)
        _serializer.is_valid()
        return Response(_serializer.data, status=200, content_type="application/json")


# Benefits
class BenefitListCreateAPIView(StaffListRetrieveMixin):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
    authentication_classes = DEFAULT_AUTH
    permission_classes = DEFAULT_PERMS
