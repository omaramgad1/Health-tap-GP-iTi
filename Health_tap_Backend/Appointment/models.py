from django.db import models
from User.models import Doctor
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, time
from django.utils import timezone


def validate_date_range(value):
    today = timezone.localdate()
    max_date = today + timezone.timedelta(days=6)
    if value < today or value > max_date:
        raise ValidationError('Date must be today or within the next 6 days')


def validate_time_range(value):
    if value < time(hour=9) or value > time(hour=23):
        raise ValidationError('Time must be between 9:00 AM and 11:00 PM')


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField(validators=[validate_date_range])
    start_time = models.TimeField(
        validators=[validate_time_range])
    price = models.DecimalField(max_digits=8, decimal_places=2)
    Status_CHOICES = (
        ('A', 'AVAILABLE'),
        ('R', 'RESERVED'),

    )
    status = models.CharField(
        max_length=1, choices=Status_CHOICES, default='A', null=True, blank=True)
    DURATION_CHOICES = (
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '1 hour'),
        (90, '1.5 hours'),
        (120, '2 hours'),
    )
    duration = models.PositiveIntegerField(choices=DURATION_CHOICES)

    class Meta:
        verbose_name_plural = 'Appointments'

    def end_time(self):
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = start_datetime + timedelta(minutes=self.duration)
        return end_datetime.time()
