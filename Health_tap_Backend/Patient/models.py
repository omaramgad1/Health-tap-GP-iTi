from django.db import models
from User.models import User, CustomUserManager


class PatientManager(CustomUserManager):

    def create_patient(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_patient', True)
        return self._create_user(email, password, **extra_fields)


class Patient(User):
    is_patient = models.BooleanField(default=True)
    objects = PatientManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}@Patient'


