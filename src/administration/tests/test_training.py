from datetime import datetime as dt
import json

from django.test import TestCase

from src.account.staff import Department
from src.administration.models import *
from src.account.models import Staff, StaffUser
from utils.base_test import (create_test_user, create_staff, add_headers, random_staffs)


class TrainingTestCase(TestCase):

    def setUp(self):
        self.user = create_test_user(StaffUser)
        self.client.login(username="1234567890", password="admin.123")
        self.staff = create_staff(Staff)
        self.staffs = random_staffs(9, Staff, Department)

    def test_training_crested(self):
        training = TrainingProgram.objects.create(
            program_name="HSE Training",
            description="Health and safety",
            start_date=dt.now(),
            end_date=dt.now(),
        )
        training.staffs.set(self.staffs)
        training.save()
        trainings = TrainingProgram.objects.all()
        self.assertTrue(trainings.count() == 1)
        self.assertTrue(training.staffs.count() == 9)
        self.assertTrue(training.staffs.count() == len(self.staffs))

    def test_training_post(self):
        data = {
            "programName": "HSE Training",
            "description": "Health and safety",
            "startDate": "2023-07-20",
            "endDate": "2023-08-10",
            "staffs": [staf.pk for staf in self.staffs]
        }
        req = self.client.post('/api/training-programs/',
                               data=data, content_type='application/json', **add_headers())
        self.assertTrue(req.status_code == 201)

#     def test_training_put(self):
#         req = self.client.get('/api/training-programs/1/', **add_headers())
#         _trainings = req.json()
#         data = {
#             "programName": "IT Training",
#             "programDescription": "IT and safety",
#             "startDate": _trainings.get('startDate'),
#             "endDate": _trainings.get('endDate'),
#             "staffs": [1, 2]
#         }
#         _req = self.client.put('/api/training-programs/1/',
#                                data=data, content_type='application/json', **add_headers())
#         self.assertEqual(_req.status_code, 200)

#     def test_training_delete(self):
#         self.client.delete('/api/training-programs/1/', **add_headers())
#         req = self.client.get('/api/training-programs/1/', **add_headers())
#         self.assertTrue(req.status_code == 404)
