from django.db import models
from User.models import Doctor
from django.core.exceptions import ValidationError
import time
from django.utils import timezone


def validate_date_range(value):
    today = timezone.localdate()
    max_date = today + timezone.timedelta(days=6)
    if value < today or value > max_date:
        raise ValidationError('Date must be today or within the next 6 days')


def validate_time_range(value):
    if value < time(hour=9) or value > time(hour=23):
        raise ValidationError('Time must be between 9:00 AM and 5:00 PM')


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField(validators=[validate_date_range])
    time = models.TimeField(validators=[validate_time_range])
    price = models.DecimalField(max_digits=8, decimal_places=2)
    Status_CHOICES = (
        ('A', 'AVAILABLE'),
        ('R', 'RESERVED'),

    )
    status = models.CharField(
        max_length=1, choices=Status_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Appointments'
