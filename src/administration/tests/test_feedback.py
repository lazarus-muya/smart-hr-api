from pprint import pprint

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse, resolve

from src.account.models import Staff, StaffUser
from src.administration.engagement import *
from utils.base_test import (create_test_user, add_headers, create_staff, random_staffs)
from src.administration.api_views import FeedbackListCreateAPIView


class EngagementTestCase(TestCase):
    def setUp(self):
        self.user = create_test_user(StaffUser)
        self.client.login(username="1234567890", password="admin.123")
        self.staff = create_staff(Staff)
    
    def _post_data(self):
        data = {
            "staff": self.staff.pk,
            "feedback": "I love the new programe",
            "date": "2023-08-22"
        }
        return self.client.post('/api/feedbacks/', data=data, **add_headers())
    
    def test_authentication(self):
        req = self.client.get('/api/feedbacks/')
        self.assertTrue(req.status_code == 401)

    def test_feedback_created(self):
        
        feedback = FeedBack.objects.create(
            staff=self.staff,
            feedback="Train new staffs",
            feedback_type=FeedbackTypes.SUGGESTION,
        )
        feedback.save()
        self.assertTrue(feedback.pk == 1)
        self.assertEqual(feedback.staff, self.staff)

    def test_feedback_post(self):
        req = self._post_data()
        self.assertTrue(req.status_code == 201)
    
    def test_feedback_get(self):
        self._post_data()
        req = self.client.get('/api/feedbacks/1/', **add_headers())
        self.assertTrue(req.status_code == 200)

    def test_feedback_put(self):
        _req = req = self._post_data()
        jsonData = _req.json()
        jsonData["feedback"] = "I love the new trainer"

        req = self.client.put('/api/feedbacks/1/', data=jsonData,
                              **add_headers(), content_type="application/json")
        updateData = req.json()
        self.assertTrue(req.status_code == 200)
        self.assertEqual(updateData["feedback"], "I love the new trainer")

    def test_feedback_patch(self):
        self._post_data()
        req = self.client.patch('/api/feedbacks/1/', data={"feedback": "I love the new trainer"},
                              **add_headers(), content_type="application/json")
        updateData = req.json()
        self.assertTrue(req.status_code == 200)
        self.assertEqual(updateData["feedback"], "I love the new trainer")

    def test_feedback_delete(self):
        self._post_data()
        req = self.client.delete('/api/feedbacks/1/', **add_headers())
        self.assertEqual(req.status_code, 204)
