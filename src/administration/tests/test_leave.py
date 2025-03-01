from datetime import datetime as dt
import json

from django.test import TestCase
from django.utils import timezone

from src.administration.models import *
from utils.options import LeaveStatus, LeaveType
from src.account.models import Staff, StaffUser
from utils.base_test import add_headers


class LeaveRequestTestCase(TestCase):
    def setUp(self):
        self.user = StaffUser.objects.create(
            phone_number=1234567890, is_superuser=True, is_staff=True, is_active=True
        )
        self.user.set_password("admin.123")
        self.user.save()

        self.client.login(username="1234567890", password="admin.123")

        self.staff = Staff.objects.create(
            staff_id="1098016210675962",
            first_name="Jane",
            middle_name="Mills",
            last_name="Doe",
            date_of_birth=timezone.now(),
            phone_number=12345689,
        )
        self.staff.save()

    def test_leave_created(self):
        leave = LeaveRequest.objects.create(
            staff=self.staff,
            leave_type=LeaveType.ANNUAL,
            status=LeaveStatus.APPROVED,
            start_date=dt(2024, 10, 20),
            end_date=dt(2024, 11, 20),
        )
        leave.save()
        self.assertTrue(leave.pk == 1)
        self.assertEqual(leave.staff, self.staff)
        self.assertTrue(leave.status == LeaveStatus.APPROVED)
        self.assertTrue(leave.leave_type == LeaveType.ANNUAL)
    
    def _post_data(self):
        data = {
            "staff": self.staff.pk,
            "leaveType": "Annual",
            "leaveStatus": "Approved",
            "startDate": "2024-08-20",
            "endDate": "2024-09-20",
        }
        return self.client.post('/api/leave-requests/', data=data, **add_headers())

    def test_leave_post(self):
        req = self._post_data()
        self.assertTrue(req.status_code == 201)

    def test_leave_get(self):
        self._post_data()
        req = self.client.get('/api/leave-requests/', **add_headers())
        data = req.json()
        self.assertEqual(req.status_code, 200)
        self.assertEqual(data[0]['staff'], self.staff.staff_id)

    def test_leave_put(self):
        # get original object
        _leave = self._post_data()
        leave = _leave.json()
        data = {
            "staff": leave["staff"],
            "leaveType": leave['leaveType'],
            "status": LeaveStatus.DONE,
            "startDate": leave["startDate"],
            "endDate": leave["endDate"]
        }
        req = self.client.put('/api/leave-requests/1/',
                              data=data, content_type="application/json", **add_headers())
        _req = self.client.get('/api/leave-requests/1/', **add_headers())
        _updated = _req.json()
        self.assertTrue(req.status_code == 200)
        self.assertTrue(_updated.get('status') == LeaveStatus.DONE)
    
    def test_patch(self):
        _leave = self._post_data()
        leave = _leave.json()
        req = self.client.patch('/api/leave-requests/1/',
                                data={"leaveType": LeaveType.SICK_LEAVE}, content_type="application/json", **add_headers())
        _req = self.client.get('/api/leave-requests/1/', **add_headers())
        _updated = _req.json()
        self.assertTrue(req.status_code == 200)
        self.assertTrue(_updated.get('leaveType') == LeaveType.SICK_LEAVE)

    def test_leave_delete(self):
        self._post_data()
        req = self.client.delete('/api/leave-requests/1/', **add_headers())
        self.assertTrue(req.status_code == 204)
        _leave = self.client.get('/api/leave-requests/1/', **add_headers())
        self.assertTrue(_leave.status_code == 404)
