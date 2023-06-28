from django.db import models
from User.models import Patient
from Appointment.models import Appointment

class Reservation(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='reservations')
    
    appointment = models.OneToOneField(Appointment,on_delete=models.CASCADE)
    
    Status_CHOICES = (
        ('F', 'FREE'),
        ('R', 'RESERVED'),
        ('C', 'CANCLED'),

    )
    status = models.CharField(max_length=1, choices=Status_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Reservations'
