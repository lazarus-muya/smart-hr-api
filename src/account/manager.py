from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class StaffUserManager(BaseUserManager):

    def create_user(self, email, phone_number, password, **extra_fields):
        if not all([email, phone_number, password]):
            raise ValueError(_("phone number, email and password are required."))
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("metadata", {})

        if extra_fields["is_staff"] == False:
            raise ValueError(_("is_staff must be set to True"))
        if extra_fields["is_superuser"] == False:
            raise ValueError(_("is_superuser must be set to True"))

        return self.create_user(email, phone_number, password, **extra_fields)
