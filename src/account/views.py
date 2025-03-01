from django.contrib.auth.models import User, Group, Permission
from rest_framework.views import APIView
from rest_framework.response import Response


class ResetPasswordView(APIView):

    def reset_password(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=401)
        user = request.user