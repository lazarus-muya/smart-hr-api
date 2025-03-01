from django.test import TestCase
from datetime import datetime as dt

from src.account.staff import Department
from src.administration.models import *
from src.account.models import Staff, StaffUser
from utils.base_test import create_test_user, add_headers, random_staffs, create_staff


class PerformanceTestCase(TestCase):
    def setUp(self):
        create_test_user(StaffUser)
        self.staff = create_staff(Staff)
        self.reviewer = Staff.objects.create(
            staff_id="1098016210675963",
            first_name="Johh",
            middle_name="Jay",
            last_name="Kahn",
            date_of_birth=timezone.now().strftime("%Y-%m-%d"),
            phone_number=12445689,
        )
        self.reviewer.save()

        department = Department.objects.create(department_name="Accounts")
        department.save()

        self.hod = HeadOfDepartment.objects.create(
            hod=self.reviewer, department=department
        )
        self.hod.save()
        self.staff.department = department
        self.reviewer.department = department
        self.reviewer.save()
        self.staff.save()

    def _post_data(self):
        data = {
            "staff": self.staff.pk,
            "score": 4,
            "hod": self.hod.pk,
            "reviewDate": dt(2023, 5, 12).date(),
            "comment": "Improved",
        }
        return self.client.post(
            "/api/performance-reviews/",
            data=data,
            content_type="application/json",
            **add_headers()
        )

    def test_create_performance(self):
        performance = PerformanceReview.objects.create(
            staff=self.staff,
            hod=self.hod,
            score=4,
            review_date=dt(2024, 5, 12).date(),
            comment="Improved",
        )
        performance.save()
        self.assertTrue(performance.hod == self.hod)
        self.assertTrue(performance.hod.department == self.staff.department)
        self.assertTrue(self.staff.reporting_to == performance.hod.hod)

    def test_performance_post(self):
        response = self._post_data()
        perf = response.json()

        self.assertTrue(response.status_code == 201)
        self.assertEqual(perf["staff"], self.staff.staff_id)
        self.assertEqual(perf["hod"], self.hod.pk)


    def test_performance_put(self):
        self._post_data()
        _perf = self.client.get('/api/performance-reviews/1/', **add_headers())
        perf = _perf.json()
        data = {
            "staff": perf['staff'],
            "score": 3,
            "hod": perf['hod'],
            "reviewDate": perf["reviewDate"],
            "comment": perf["comment"],
        }
        response = self.client.put('/api/performance-reviews/1/', data=data,
                                   content_type='application/json', **add_headers())
        _response = response.json()
        self.assertTrue(response.status_code == 200)
        self.assertTrue(_response["score"] == 3)
    
    def test_performance_patch(self):
        self._post_data()
        _perf = self.client.get('/api/performance-reviews/1/', **add_headers())
        req = self.client.patch('/api/performance-reviews/1/', data={"score": 1}, content_type="application/json", **add_headers())
        _req = self.client.get('/api/performance-reviews/1/', **add_headers())

        self.assertTrue(req.status_code == 200)
        self.assertTrue(_req.json()["score"] == 1)

    def test_performance_delete(self):
        self._post_data()
        response = self.client.delete('/api/performance-reviews/1/', **add_headers())
        self.assertEqual(response.status_code, 204)
        _response = self.client.get('/api/performance-reviews/1/', **add_headers())
        self.assertTrue(_response.status_code == 404)
