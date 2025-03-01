import json
from rest_framework.test import APITestCase

from src.account.models import StaffUser
from src.account.staff import Staff
from src.administration.engagement import Survey, SurveyResponse
from utils.base_test import add_headers, create_test_user, create_staff


class SurveyResponseTest(APITestCase):
    def setUp(self):
        self.user = create_test_user(StaffUser)
        self.client.login(username="1234567890", password="admin.123")
        self.staff = create_staff(Staff)
    
    def _post_data(self):
        data = {
            "title": "Test Survey",
            "question": "Will this pass",
            "description": "some test info",
            "startDate": "2024-07-20",
            "endDate": "2024-08-30",
            "isActive": True
        }
        return self.client.post('/api/surveys/', data=json.dumps(data), **add_headers(), content_type="application/json")

    def test_survey_created(self):
        survey = Survey.objects.create(
            title="Test Survey",
            question="Will this pass?",
            description="some test info",
            start_date="2024-07-20",
            end_date="2024-08-30",
            is_active=True
        )
        survey.save()
        self.assertTrue(survey.pk == 1)


    def test_survey_post(self):
        req = self._post_data()
        self.assertEqual(req.status_code, 201)
    
    def test_survey_get(self):
        self._post_data()
        req = self.client.get('/api/surveys/', **add_headers())
        self.assertEqual(req.status_code, 200)
        self.assertEqual(len(req.json()), 1)

    def test_response_post(self):
        survey = self._post_data()
        data = {
            "staff": self.staff.pk,
            "survey": survey.json()["id"],
            "response": "This is a response"
        }
        req = self.client.post('/api/survey-responses/',
                               data=json.dumps(data), **add_headers(), content_type="application/json")
        jsonData = req.json()
        self.assertEqual(req.status_code, 201)
        self.assertEqual(jsonData["staff"], self.staff.pk)
        self.assertEqual(jsonData["survey"], survey.json()["id"])

    def test_response_put(self):
        survey = self._post_data()
        data = {
            "staff": self.staff.pk,
            "survey": survey.json()["id"],
            "response": "This is a response"
        }
        req = self.client.post('/api/survey-responses/',
                               data=json.dumps(data), **add_headers(), content_type="application/json")
        
        _data = {
            "staff": req.json()["staff"],
            "survey": req.json()["survey"],
            "response": "This is updated response"
        }
        req = self.client.put('/api/survey-responses/1/',
                              data=json.dumps(_data), **add_headers(), content_type="application/json")

        jsonData = req.json()
        self.assertEqual(req.status_code, 200)
        self.assertEqual(jsonData["response"], "This is updated response")

    def test_response_delete(self):
        survey = self._post_data()
        data = {
            "staff": self.staff.pk,
            "survey": survey.json()["id"],
            "response": "This is a response"
        }
        self.client.post('/api/survey-responses/',
                               data=json.dumps(data), **add_headers(), content_type="application/json")
               
        res = self.client.delete('/api/survey-responses/1/', **add_headers())
        self.assertTrue(res.status_code == 204)
