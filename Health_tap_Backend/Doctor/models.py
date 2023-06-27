from django.db import models
from Specialization.models import Specialization
import re
from django.core.exceptions import ValidationError
from User.models import User
from City.models import City
from District.models import District


def validate_profLicenseNum(value):
    # Regular expression pattern to match the desired pattern
    pattern = r'^[02468]{2}[13579]{2}\d{2}$'

    # Check if the value matches the pattern
    if re.match(pattern, value) == False:
        raise ValidationError("profession License Number Invalid.")


class Doctor(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='doctor')
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE, related_name='doctors')
    profLicenseNo = models.CharField(
        max_length=6, validators=[validate_profLicenseNum])
    city = models.OneToOneField(
        City, on_delete=models.CASCADE, related_name='doctors')
    district = models.OneToOneField(
        District, on_delete=models.CASCADE, related_name='doctors')
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}@Doctor@({self.profLicenseNo})'

    def save(self, *args, **kwargs):
        if not self.pk:  # if object is being created
            self.user.is_active = False
            self.user.is_doctor = True
        self.user.save()
        super().save(*args, **kwargs)
