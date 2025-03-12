import datetime
from django.conf import settings
from utils.constants import REFRESH_TOKEN_EXPIRY, TOKEN_EXPIRY


# REST FRAMEWORK [JSONParser, CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer]
REST_FRAMEWORK = {
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'rest_framework_filters.backends.RestFrameworkFilterBackend',
    # ),
    "DEFAULT_RENDERER_CLASSES": (
        # 'rest_framework.parsers.JSONParser',
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        # 'rest_framework.parsers.JSONParser',
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DATE_INPUT_FORMATS": ["%Y-%m-%d", "iso-8601"],
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "TIME_FORMAT": "%H:%M:%S",
}

JWT_AUTH = {
    "JWT_SECRET_KEY": settings.SECRET_KEY,
    "JWT_EXPIRATION_DELTA": TOKEN_EXPIRY,
    "JWT_REFRESH_EXPIRATION_DELTA": REFRESH_TOKEN_EXPIRY,
    "JWT_ALGORITHM": "HS256",
    "JWT_TOKEN_ID": "include",
    "JWT_ENCODE_HANDLER": "rest_framework_jwt.utils.jwt_encode_payload",
    "JWT_DECODE_HANDLER": "rest_framework_jwt.utils.jwt_decode_token",
    "JWT_PAYLOAD_HANDLER": "rest_framework_jwt.utils.jwt_create_payload",
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": "rest_framework_jwt.utils.jwt_get_username_from_payload_handler",
    "JWT_PAYLOAD_INCLUDE_USER_ID": True,
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LEEWAY": 0,
    "JWT_ALLOW_REFRESH": True,
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
    "JWT_RESPONSE_PAYLOAD_HANDLER": "rest_framework_jwt.utils.jwt_create_response_payload",
    "JWT_AUTH_COOKIE_PATH": "/",
    "JWT_AUTH_COOKIE_SECURE": True,
    "JWT_AUTH_COOKIE_SAMESITE": "Lax",
    "JWT_DELETE_STALE_BLACKLISTED_TOKENS": False,
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
RESEND_SMTP_PORT = 587
RESEND_SMTP_USERNAME = "resend"
RESEND_SMTP_HOST = "smtp.resend.com"
# EMAIL_USE_SSL = True
# EMAIL_USE_TLS = False
# DEFAULT_FROM_EMAIL = ''
