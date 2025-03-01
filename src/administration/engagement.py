from collections.abc import Iterable
from django.db import models

from utils.options import YesNoOptions, FeedbackTypes, RatingChoices
from utils.helpers import random_int_id
# from src.account.models import Staff

Qs = models.QuerySet


class FeedBack(models.Model):
    staff = models.ForeignKey("account.Staff", on_delete=models.SET_NULL, null=True, blank=True)
    feedback = models.TextField(max_length=1000)
    feedback_type = models.CharField(
        max_length=20, choices=FeedbackTypes.choices, default=FeedbackTypes.OTHER
    )
    date = models.DateField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        if not self.staff:
            return "Anonymous user - {}".format(random_int_id(10))
        return self.staff.full_name

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def save(self, *args, **kwargs) -> None:
        if not self.staff:
            self.is_anonymous = True
        return super().save(*args, **kwargs)


"""
    Question model was ignored and serves no purpose.
    It will be removed in future.
"""

class Question(models.Model):
    question = models.TextField(max_length=500)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Survey(models.Model):
    survey_id = models.CharField(max_length=12, default=random_int_id(12))
    title = models.CharField(max_length=100)
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question = models.TextField(max_length=500)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    @property
    def list_survey_responses(self) -> Qs:
        return self.surveyresponse_set.all()


class SurveyResponse(models.Model):
    staff = models.ForeignKey("account.Staff", on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.staff.full_name

    class Meta:
        verbose_name = "Survey Response"
        verbose_name_plural = "Survey Responses"
