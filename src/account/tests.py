from django.test import TestCase
from datetime import datetime as dt
# from django.contrib.auth.hashers import check_password
from rest_framework.test import APIClient, APIRequestFactory

from .models import *
from src.account.staff import *
from src.account.models import StaffUser

# from utils.base_test import create_test_user, add_headers, random_staffs, create_staff



class AccountsTestCase(APIClient):
    def setUp(self):
        self.user = StaffUser.objects.create(
            phone_number=1234567890, is_superuser=True, is_staff=True, is_active=True
        )
        self.user.set_password("admin.123")
        self.user.save()

        self.logged_in = self.client.login(username="1234567890", password="admin.123")

    def test_login(self):
        self.assertEqual(self.logged_in, True)

    def test_staff_and_user_create(self):
        staff = Staff.objects.create(
            staff_id="1098016210675962",
            first_name="Jane",
            middle_name="Mills",
            last_name="Doe",
            date_of_birth=dt.now(),
            phone_number=12345689,
        )
        staff.save()

        staff_user = StaffUser.objects.filter(phone_number=12345689)
        self.assertTrue(staff_user.exists())
        self.assertEqual(
            check_password(
                f"{staff.last_name.lower()}_{staff.phone_number}",
                staff_user.first().password,
            ),
            True,
        )
        self.assertFalse(staff_user.first().is_superuser)
        self.assertEqual(staff.first_name, "Jane")

    def test_staff_update(self):
        staff = Staff.objects.create(
            staff_id="1098016210675962",
            first_name="Jane",
            middle_name="Mills",
            last_name="Doe",
            date_of_birth=dt.now(),
            phone_number=12345689,
        )
        staff.save()
        staff.first_name = "John"
        staff.save()
        self.assertEqual(staff.first_name, "John")

    def test_staff_delete(self):
        staff = Staff.objects.create(
            staff_id="1098016210675962",
            first_name="Jane",
            middle_name="Mills",
            last_name="Doe",
            date_of_birth=dt.now(),
            phone_number=12345689,
        )
        staff.save()
        staff.delete()
        self.assertEqual(Staff.objects.count(), 0)

    def test_staff_list(self):
        staff = Staff.objects.create(
            staff_id="1098016210675962",
            first_name="Jane",
            middle_name="Mills",
            last_name="Doe",
            date_of_birth=dt.now(),
            phone_number=12345689,
        )
        staff.save()
        self.assertEqual(Staff.objects.count(), 1)

    def test_staff_department(self):
        staff = Staff.objects.create(
            staff_id="1098016210675962",
            first_name="Jane",
            middle_name="Mills",
            last_name="Doe",
            date_of_birth=dt.now(),
            phone_number=12345689,
        )
        staff.save()
        department = Department.objects.create(department_name="Accounts")
        department.save()
        staff.department = department
        staff.save()
        self.assertEqual(staff.department.department_name, "Accounts")

    def test_staff_hod(self):
        staff = Staff.objects.create(
            staff_id="1098016210675962",
            first_name="Jane",
            middle_name="Mills",
            last_name="Doe",
            date_of_birth=dt.now(),
            phone_number=12345689,
        )
        staff.save()
        department = Department.objects.create(department_name="Accounts")
        department.save()
        staff.department = department
        staff.save()
        hod = HeadOfDepartment.objects.create(hod=staff, department=department)
        hod.save()

        new_staff = Staff.objects.create(
            first_name="John",
            middle_name="Py",
            last_name="Node",
            date_of_birth=dt.now(),
            phone_number=12345677,
        )
        new_staff.save()
        new_staff.department = department
        new_staff.save()

        self.assertEqual(new_staff.reporting_to, staff)
        self.assertEqual(hod.hod.first_name, "Jane")

    def test_department_create(self):
        department = Department.objects.create(department_name="Accounts").save()
        self.assertEqual(Department.objects.count(), 1)

    def test_department_update(self):
        department = Department.objects.create(department_name="Accounts")
        department.save()
        department.department_name = "HR"
        department.save()
        self.assertEqual(Department.objects.first().department_name, "Hr")

    def test_department_delete(self):
        department = Department.objects.create(department_name="Accounts")
        department.save()
        department.delete()
        self.assertEqual(Department.objects.count(), 0)

    def test_staff_bank(self):
        staff = Staff.objects.create(
            staff_id="1098016210675962",
            first_name="Jane",
            middle_name="Mills",
            last_name="Doe",
            date_of_birth=dt.now(),
            phone_number=12345689,
        )
        staff.save()
        bank = Bank.objects.create(bank_name="Access Bank")
        bank.save()
        staff.bank = bank
        staff.save()
        self.assertEqual(staff.bank.bank_name, "Access Bank")
    
    # def test_staff_post(self):
        staff = {
            "staff_id": "1098016210675962",
            "first_name": "Jane",
            "middle_name": "Mills",
            "last_name": "Doe",
            "date_of_birth": dt.now(),
            "phone_number": 12345689,
        }
        url = "/api/staff/"
        response = self.client.post(url, staff, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

