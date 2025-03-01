import base64
import random
import string
from datetime import datetime as dt
from django.utils import timezone


""" This are reusable methods """


def create_test_user(StaffUser):
    _user = StaffUser.objects.create(
        is_active=True, is_staff=True, is_superuser=True, phone_number=1234567890
    )
    _user.set_password("admin.123")
    _user.save()


def add_headers() -> dict:
    _creds = "1234567890:admin.123"
    return {"HTTP_AUTHORIZATION": f"Basic {base64.b64encode(_creds.encode()).decode()}"}


def create_staff(Staff):
    _staff = Staff(
        staff_id="1098016210675962",
        first_name="Jane",
        middle_name="Mills",
        last_name="Doe",
        date_of_birth=timezone.now(),
        phone_number=12345689,
    )
    _staff.save()
    return _staff


def random_staffs(count, Staff, Department):
    departments = Department.objects.bulk_create(
        [
            Department(department_name="Administration"),
            Department(department_name="Accounts"),
            Department(department_name="Hr Department"),
        ]
    )

    staffs = []

    for i in range(count):
        staff = Staff(
            staff_id="".join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            first_name="Test",
            middle_name=f"User {i}",
            last_name=f"Staff {i}",
            department=random.choice(departments),
            phone_number=int("".join(random.choices(string.digits, k=10))),
            date_of_birth=dt.now(),
        )
        staff.save()
        staffs.append(staff)

    return staffs
