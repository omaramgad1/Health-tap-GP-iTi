from django.db import models
from Patient.models import Patient
from Doctor.models import Doctor

# Create your models here.

class Review(models.Model):
    Rate = models.IntegerField(max_length=5)
    comment = models.CharField(max_length=70)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE ,related_name="patient_reviews")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_reviews")
    
class Meta:
        verbose_name_plural = 'Reviews'