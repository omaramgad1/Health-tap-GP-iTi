import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _
from Specialization.models import Specialization
import cloudinary.api
from cloudinary.models import CloudinaryField, CloudinaryResource
from City.models import City
from District.models import District




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
        if not validate_password(password):
            raise ValueError('Password is invalid')
        
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

def validate_profLicenseNum(value):
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


def validate_egypt_national_id(value):
    if len(value) != 14:
        raise ValidationError('National ID must be 14 digits long')
    if not value.isdigit():
        raise ValidationError('National ID must consist of digits only')
    if value[0] not in ['2', '3', '5']:
        raise ValidationError("Invalid Egyptian National ID number.")
    if value[1] not in ['0', '1', '2', '3', '4', '9']:
        raise ValidationError("Invalid Egyptian National ID number.")

def validateImage(image):
    if not isinstance(image, CloudinaryResource):
        # The image is not a Cloudinary resource, so we can't validate it
        return

    info = cloudinary.api.resource(image.public_id)
    file_size = info.get("bytes")
    if not file_size:
        raise ValidationError('Failed to get image size.')

    print(file_size)
    if file_size > 2 * 1024 * 1024:
        raise ValidationError('Image size should be less than 2MB.')

    file_extension = image.format.lower()
    if file_extension not in ['png', 'jpg', 'jpeg']:
        raise ValidationError('Only PNG, JPG, and JPEG images are allowed.')


def validate_gender(value):
    if value not in ['m', 'male', 'f', 'female' , 'M' , "Male",'F' , 'Female']:
        raise ValidationError('Invalid gender value')
    

def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long')
    if not any(c.isdigit() for c in value):
        raise ValidationError('Password must contain at least one digit')

def validate_phone_number(value):
    pattern =r'^(\+201|00201|01)?(0|1|2)[0-9]{8}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid phone number format.')
        # +201033022410
        # 01033022410
        
class User(AbstractBaseUser, PermissionsMixin):
    # Abstractbaseuser has password, last_login, is_active by default
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    date_of_birth = models.DateField(
        null=True, blank=True, validators=[validate_date_of_birth])
    phone = models.CharField(max_length=15 , validators=[validate_phone_number], unique=True)
    national_id = models.CharField(max_length=14, unique=True , validators=[
                                   validate_egypt_national_id])
    profileImgUrl = CloudinaryField('images', validators=[validateImage])
    password = models.CharField(validators=[validate_password], max_length=128)
    confirm_password = models.CharField(max_length=128)
    gender = models.CharField(max_length=6, validators=[validate_gender])

    # validators=[validate_image]
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # must needed, otherwise you won't be able to loginto django-admin.
    is_staff = models.BooleanField(default=False)
    # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True)
    # this field we inherit from PermissionsMixin.
    is_superuser = models.BooleanField(default=False)


# ###############################
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
# 'first_name', 'last_name','phone'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        super().clean()
        if self.password != self.confirm_password:
            raise ValidationError('Passwords do not match!')
        
        if self.password < 8:
            raise ValidationError('Password must be at least 8 characters long')
        if not any(c.isdigit() for c in self.password):
            raise ValidationError('Password must contain at least one digit')


    def __str__(self):
        return self.first_name


