# views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest

# from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import *

from .utils.email import send_email
from src.account.serializers import UserSerializer
from .utils.constants import *


User = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        phone_number = self.request.query_params.get("phone_number")
        if not phone_number:
            return Response(
                {"code": FIELD_MISSING, "message": "Phone number is required."}
            )
        try:
            user = User.objects.get(phone_number=phone_number)
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response(
                {"": USER_DOES_NOT_EXISTS, "message": "User does not exist."}
            )

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        email = request.data.get("email")
        password = request.data.get("password")
        is_admin = str(request.data.get("is_admin", "False")).lower() == "true"

        if not all([phone_number, email, password]):
            return Response(
                {"code": FIELD_MISSING, "error": "Missing required fields"}, status=400
            )
        try:
            db_user = User.objects.filter(phone_number=phone_number)
            if db_user.exists():
                return Response(
                    {
                        "code": USER_EXISTS,
                        "message": "User with this phone number already exists.",
                    }
                )
            user = User.objects.create(
                phone_number=phone_number, email=email, password=password
            )
            user.is_active = True
            if is_admin:
                user.is_superuser = True
            user.save()
            return Response({"code": SUCCESS, "user": UserSerializer(user).data})
        except Exception as e:
            return Response({"code": AUTH_EXCEMPTION, "error": str(e)})


# Create UserLogin View
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {
                    "code": FIELD_MISSING,
                    "error": "Phone number and password are required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=email, password=password)

        if user is not None:
            return Response(
                {
                    "code": SUCCESS,
                    "user": UserSerializer(user).data,
                    "message": "Login successful",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"code": AUTH_EXCEMPTION, "error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# UserLogout View
class UserLogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(
            {"message": "Successfully logged out."}, status=status.HTTP_200_OK
        )


# ChangePasswordView
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not request.user.is_authenticated:
            return Response(
                {"code": AUTH_EXCEMPTION, "message": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not all([old_password, new_password]):
            return Response(
                {
                    "code": FIELD_MISSING,
                    "message": "Old password and new password are required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = request.user

        if not user.check_password(old_password):
            return Response(
                {"code": AUTH_EXCEMPTION, "message": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "Password successfully changed."}, status=status.HTTP_200_OK
        )


# PasswordResetView
class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        email = request.data.get("email")
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response(
                {"message": "Email address or Phone Number not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = request.build_absolute_uri("/")
        reset_link = "{}/reset-password/{}/{}/".format(url, uid, token)

        email_response = send_email(
            recipient_list=[email],
            subject="Password Reset",
            message=reset_link,
            from_email="info@dategroupafrica.com",
            attachments=[],
            cc_list=[],
        )

        if email_response["code"] != 0:
            return Response(
                {
                    "status": "Failed to send email",
                    "code": email_response["code"],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "status": "Password reset link sent to your email.",
                "code": 0,
                "response": email_response,
            },
            status=status.HTTP_200_OK,
        )


# PasswordResetConfirmView
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"message": "Invalid token or user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Password successfully reset."}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST
        )
