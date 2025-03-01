from rest_framework import permissions, authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# from rest_framework_filters.backends import DjangoFilterBackend

DEFAULT_AUTH = [authentication.TokenAuthentication, authentication.BasicAuthentication, JSONWebTokenAuthentication]
DEFAULT_PERMS = [permissions.IsAuthenticated, permissions.IsAdminUser]
# DEFAULT_AUTH  = [];
# DEFAULT_PERMS = [];
# DEFAULT_FILTER_BACKENDS = (DjangoFilterBackend, )

LOGGER_VERSION = 1
LOGGER_LEVEL = {
    "info": "INFO",
    "warning": "WARNING",
}

""" 
    - FileHandler(filename, mode='a', encoding=None, delay=False, errors=None)
    - HTTPHandler(host, url, method='GET', secure=False, credentials=None, context=None) 
    - SMTPHandler(mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None, timeout=1.0) 
"""
DEFAULT_FILE_LOGGER = "logging.FileHandler"
EMAIL_LOGGER = "SMTPHandler"  # send logs to enmail
WEB_LOGGER = "logging.HTTPHandler"

""" : Output logger files"""
LOGGER_FILENAMES = {
    "settings": "logs/system-settings.log",
    "users": "logs/users-logs.log",
    "staffs": "logs/staff-logs.log",
    "documents": "logs/directory-logs.log",
}
