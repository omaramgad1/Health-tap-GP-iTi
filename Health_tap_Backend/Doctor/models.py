from django.db import models
from Specialization.models import Specialization
import re
from django.core.exceptions import ValidationError
from User.models import User, CustomUserManager
from City.models import City
from District.models import District


def validate_profLicenseNum(value):
    # Regular expression pattern to match the desired pattern
    pattern = r'^[02468]{2}[13579]{2}\d{2}$'

    # Check if the value matches the pattern
    if re.match(pattern, value) == False:
        raise ValidationError("profession License Number Invalid.")


class DoctorManager(CustomUserManager):

    def create_doctor(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_doctor', True)
        return self._create_user(email, password, **extra_fields)


class Doctor(User):
    is_doctor = models.BooleanField(default=True)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE, related_name='Specialization')
    profLicenseNo = models.CharField(
        max_length=6, validators=[validate_profLicenseNum])
    city = models.ForeignKey(
            City, on_delete=models.CASCADE, related_name='doctorsByCity')
    district = models.ForeignKey(
            District, on_delete=models.CASCADE, related_name='doctorsByDistrict')
    address = models.CharField(max_length=255, null=True, blank=True)
    objects = DoctorManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.profLicenseNo}) @Doctor'

