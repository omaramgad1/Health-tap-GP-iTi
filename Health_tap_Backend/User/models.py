import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _
from Specialization.models import Specialization


def validate_profLicenseNum(value):
    # Regular expression pattern to match the desired pattern
    pattern = r'^[02468]{2}[13579]{2}\d{2}$'

    # Check if the value matches the pattern
    if re.match(pattern, value) == False:
        raise ValidationError("profession License Number Invalid.")


def validate_date_of_birth(value):
    today = date.today()
    age_limit = timedelta(days=365*18)
    if value > today:
        raise ValidationError('Date of birth cannot be in the future.')
    elif today - value < age_limit:
        raise ValidationError('You must be at least 12 years old to register.')


# def validate_egypt_national_id(value):
#     if not isinstance(value, str):
#         raise ValidationError('National ID must be a string')
#     if len(value) != 14:
#         raise ValidationError('National ID must be 14 digits')
#     if not value.isdigit():
#         raise ValidationError('National ID must consist of digits only')
#     if int(value[0]) % 2 == 0:
#         if not value[7:9] in ('01', '03', '05', '07', '09', '11'):
#             raise ValidationError('Invalid national ID')
#     else:
#         if not value[7:9] in ('02', '04', '06', '08', '10', '12'):
#             raise ValidationError('Invalid national ID')


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, password2=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            # first_name=first_name,
            # last_name=last_name,
            # phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, password2=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, password2, **extra_fields)

    def create_superuser(self, email, password=None, password2=None, ** extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser has to have the is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "superuser has to have the is_superuser being True")

        return self._create_user(email, password, password2,  **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # Abstractbaseuser has password, last_login, is_active by default
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    date_of_birth = models.DateField(
        null=True, blank=True, validators=[validate_date_of_birth])
    phone = PhoneNumberField(region='EG', unique=True)
    national_id = models.CharField(max_length=14)                           
    profileImgUrl = models.ImageField(
        upload_to='profileImages/', blank=True)
    # validators=[validate_image]
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # must needed, otherwise you won't be able to loginto django-admin.
    is_staff = models.BooleanField(default=False)
    # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True)
    # this field we inherit from PermissionsMixin.
    is_superuser = models.BooleanField(default=False)
#################################
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
###############################
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']
# 'first_name', 'last_name','phone'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name


class Patient(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE, related_name='Patient')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Doctor(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE, related_name='Doctor')
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE, related_name='Specialization')
    profLicenseNo = models.CharField(
        max_length=6, validators=[validate_profLicenseNum])

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.profLicenseNo})'
