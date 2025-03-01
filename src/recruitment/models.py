from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from utils.helpers import random_int_id

from utils.options import (GeneralStatus, JobSources, InterviewStatus,
                           JobStatus, InterviewTypes, RecruitmentStatus)
from src.account.staff import Department


class Candidate(models.Model):
    first_name  = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name   = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address     = models.CharField(max_length=255, null=True, blank=True)
    resume      = models.FileField(upload_to='files/applications/resumes/')
    cover_letter    = models.FileField(upload_to='files/applications/cover_letters/', null=True, blank=True)
    source  = models.CharField(max_length=255, choices=JobSources.choices, default=JobSources.OTHER)
    status  = models.CharField(max_length=50, choices=GeneralStatus.choices, default=GeneralStatus.DEFAULT)
    notes   = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def candidate_applications(self):
        return self.application_set.all()

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"


class JobPosition(models.Model):
    job_number = models.CharField(max_length=16, default=random_int_id(10))
    title = models.CharField(max_length=255)
    description = models.TextField(verbose_name=_(
        "job description separated by hyphen(-)"))
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    skills = models.TextField(verbose_name=_("skills separated by hyphen(-)"))
    experience_level = models.CharField(max_length=100, null=True, blank=True)
    salary_range = models.CharField(max_length=30, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=JobStatus.choices, default=JobStatus.CLOSED)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Job Position"
        verbose_name_plural = "Job Positions"


class Interview(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    interviewers = models.ManyToManyField("account.Staff", related_name='interviews')
    interview_date = models.DateTimeField()
    interview_type = models.CharField(
        max_length=12, choices=InterviewTypes.choices, default=InterviewTypes.ON_SITE)
    feedback = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=InterviewStatus.choices, default=InterviewStatus.SCHEDULED)

    class Meta:
        ordering = ['-interview_date']
        verbose_name = "Interview"
        verbose_name_plural = "Interviews"

 
class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=15, choices=GeneralStatus.choices, default=GeneralStatus.SUBMITTED)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.candidate.full_name

    class Meta:
        ordering = ["-application_date"]
        verbose_name = "Application"
        verbose_name_plural = "Applications"


class Vacancy(models.Model):
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    number_of_openings = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=12, choices=JobStatus.choices, default=JobStatus.OPEN)

    def __str__(self):
        return self.job_position.title

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

class Recruit(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default=RecruitmentStatus.UNDER_REVIEW, choices=GeneralStatus.choices)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.interview.candidate.full_name

    class Meta:
        verbose_name = "Recruit"
        verbose_name_plural = "Recruits"