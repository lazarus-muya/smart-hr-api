from rest_framework import routers

from src.account.api_views import (
    DepartmentListCreateAPIView,
    StaffListCreateAPIView,
    UserListCreateAPIView,
)
from src.directory.views import DocumentViewset, TransmitalViewset
from src.finance.api_views import (
    AllowanceApiView,
    BenefitListCreateAPIView,
    DeductionApiView,
    PayrollRecordListCreateAPIView,
    SalaryComponentListCreateAPIView,
    SalaryStructureListCreateAPIView,
    TaxInformationListCreateAPIView,
)

from src.administration.api_views import *


router = routers.DefaultRouter()

router.register(r"departments", DepartmentListCreateAPIView, basename="departments")
router.register(r"documents", DocumentViewset, basename="documents")
router.register(r"transmitals", TransmitalViewset, basename="transmitals")
router.register(
    r"salary-structures", SalaryStructureListCreateAPIView, basename="salary-structure"
)
router.register(
    r"salary-components", SalaryComponentListCreateAPIView, basename="salary-component"
)
router.register(r"staffs", StaffListCreateAPIView, basename="staffs")
router.register(
    r"payroll-records", PayrollRecordListCreateAPIView, basename="payroll-record"
)
router.register(
    r"time-attendance", AttendanceListCreateAPIView, basename="time-attendance"
)
router.register(
    r"leave-requests", LeaveRequestListCreateAPIView, basename="leave-request"
)
router.register(
    r"tax-information", TaxInformationListCreateAPIView, basename="tax-information"
)
router.register(r"benefits", BenefitListCreateAPIView, basename="benefit")
router.register(
    r"training-programs", TrainingProgramListCreateAPIView, basename="training-program"
)
router.register(r"deductions", DeductionApiView, basename="deductions")
router.register(r"allowances", AllowanceApiView, basename="allowances")
router.register(
    r"performance-reviews",
    PerformanceReviewListCreateAPIView,
    basename="performance-review",
)
router.register(r"users", UserListCreateAPIView, basename="user")
router.register(r"feedbacks", FeedbackListCreateAPIView, basename="feedbacks")
router.register(r"surveys", SurveyListCreateAPIView, basename="surveys")
router.register(
    r"survey-responses", SurveyResponseListCreateAPIView, basename="survey-responses"
)
router.register(r"questions", QuestionListCreateAPIView, basename="questions")

urlpatterns = router.urls
