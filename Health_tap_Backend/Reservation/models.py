from django.db import models
from Patient.models import Patient
from Appointment.models import Appointment
from django.utils import timezone


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
        appointment_end_time = self.appointment.end_time()
        current_time = timezone.now().time()

        if current_time > appointment_end_time and self.status != 'D':
            self.status = 'D'

        super().save(*args, **kwargs)
