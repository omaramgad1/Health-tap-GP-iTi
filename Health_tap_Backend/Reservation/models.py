from django.db import models
from Patient.models import Patient
from Appointment.models import Appointment
from django.utils import timezone
from datetime import datetime, timedelta

class Reservation(models.Model):
    # patient = models.ForeignKey(
    #     Patient, on_delete=models.CASCADE, related_name='reservations')

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='reservations')
    # appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name='reservation_data')

    Status_CHOICES = (
        ('R', 'RESERVED'),
        ('C', 'CANCELED'),
        ('D', 'DONE'),
    )
    status = models.CharField(
        max_length=1, choices=Status_CHOICES, default='R', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Reservations'

    def save(self, *args, **kwargs):
        current_time = timezone.now().time()
        current_date = timezone.now().date()
        appointment_start_time = self.appointment.start_time
        appointment_date = self.appointment.date
        appointment_end_time = (datetime.combine(appointment_date, appointment_start_time) + timedelta(minutes=self.appointment.duration)).time()

        if current_date > appointment_date or (current_date == appointment_date and current_time >= appointment_end_time):
            self.status = 'D'

        super().save(*args, **kwargs)