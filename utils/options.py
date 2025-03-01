from django.db import models


class GenderChoices(models.TextChoices):
    DEFAULT = "Not Specified"
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Othe"


class StaffStatus(models.TextChoices):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    TERMINATED = "Terminated"
    ON_HOLD = "On Hold"


class LeaveType(models.TextChoices):
    ANNUAL = "Annual"
    PATERNITY = "Paternity"
    MATERNITY = "Maternity"
    SICK_LEAVE = "Sick Leave"
    COMPERSORY_LEAVE = "Compensatory Leave"


class LeaveStatus(models.TextChoices):
    DONE = ("Done",)
    ON_HOLD = "On Hold"
    PENDING = "Pending"
    APPROVED = "Approved"
    CANCELED = "Canceled"
    UNDER_REVIEW = "Under Review"


class SalaryTypes(models.TextChoices):
    DAILY = "Daily"
    HOURLY = "Hourly"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"


class PaymentMethods(models.TextChoices):
    CASH = "Cash"
    CHEQUE = "Cheque"
    BANK = "Bank"
    VOUCHER = "Voucher"


class AllowanceChoices(models.TextChoices):
    HOUSE = "House Allowance"
    TRANSPORT = "Transport Allowance"
    MEDICAL = "Medical Allowance"
    DEFAULT = "Other Allowance"


class MonthsOptions(models.TextChoices):
    JAN = "January"
    FEB = "February"
    MAR = "March"
    APR = "April"
    MAY = "MAY"
    JUN = "June"
    JUL = "July"
    AUG = "August"
    SEP = "September"
    OCT = "Octomber"
    NOV = "November"
    DEC = "December"


class GeneralStatus(models.TextChoices):
    DEFAULT = "Default"
    IN_REVIEW = "In Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    DISPOSED = "Disposed"
    DISPATCHED = "Dispatched"


class DocumentType(models.TextChoices):
    ID = "Id"
    DEFAULT = "General Document"
    RESUME = "Resume"
    CERTIFICATE = "Certificate"
    CONTRACT = "Contract"
    PAYSLIP = "Payslip"
    TRANSMITAL = "Transmital"
    APPLICATION = "Application"
    PURCHASE_ORDER = "Purchase Order"
    INVOICE = "Invoice"
    TAX_FORM = "Tax Form"
    MEMO = "Memo"
    AUDIT_DOCUMENT = "Audit Document"
    OFFER_LETTER = "Offer Letter"


class JobSources(models.TextChoices):
    OTHER = "Other"
    JOB_BOARD = "Job Board"
    REFERRAL = "Referral"
    WEB_SEARCH = "Web Search"


class JobStatus(models.TextChoices):
    OPEN = "Open"
    CLOSED = "Closed"


class InterviewTypes(models.TextChoices):
    ON_SITE = "On Site"
    ONLINE = "Online"


class InterviewStatus(models.TextChoices):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    REJECTED = "Rejected"


class FormType(models.TextChoices):
    HR_FORM = "HR Form"
    JOB_APPLICATION = "Job Application"
    LEAVE_APPLICATION = "Leave Application"
    SPECIAL_REQUEST_FORM = "Request Form"
    CASH_REQUEST_FORM = "Cash Request Form"
    CASH_ADVANCED_REQUEST_FORM = "Cash Request Request Form"
    GENERAL_FORM = "General Form"


class TransmitalReasons(models.TextChoices):
    DEFAULT = "Un-specified"
    REVIEW = "Review"
    APPROVAL = "Approval"
    DISPOSAL = "Disposal"
    DISTRIBUTION = "Distribution"


class YesNoOptions(models.TextChoices):
    YES = "Yes"
    NO = "No"


class FeedbackTypes(models.TextChoices):
    COMMENDATION = "Commendation"
    CRITICISM = "Criticism"
    SUGGESTION = "Suggestion"
    OTHER = "Other"


class RatingChoices(models.IntegerChoices):
    POOR = 1, "Poor"
    BELOW_AVERAGE = 2, "Below Average"
    AVERAGE = 3, "Average"
    GOOD = 4, "Good"
    EXCELLENT = 5, "Excellent"


class EducationLevels(models.TextChoices):
    DEFAULT = "No Degree"
    CERTIFICATE = "Certificate"
    HIGH_SCHOOL = "High School"
    COLLEGE = "College"
    DIPLOMA = "Diploma"
    BACHELOR = "Bachelor"
    DEGREE = "degree"
    MASTERS = "Masters"
    DOCTORATE = "Doctorate"
    OTHER = "Other"

class RecruitmentStatus(models.TextChoices):
    UNDER_REVIEW = "Under Review"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    HIRED = "Hired"
