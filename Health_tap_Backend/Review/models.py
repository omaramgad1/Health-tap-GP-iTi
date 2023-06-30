from django.db import models
from Patient.models import Patient
from Doctor.models import Doctor

# Create your models here.

class Review(models.Model):
    RATE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rate = models.IntegerField(choices=RATE_CHOICES,default='1')
    comment = models.TextField(max_length=150)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE ,related_name="patient_reviews")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_reviews")
    
class Meta:
        verbose_name_plural = 'Reviews'