from django.db import models
from User.models import User


class Patient(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='patient')

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}@patient'

    def save(self, *args, **kwargs):
        if not self.pk:  # if object is being created
            self.user.is_active = False
            self.user.is_patient = True
        self.user.save()
        super().save(*args, **kwargs)


# class PatientManager(models.Manager):
#     def get_queryset(self, *args,  **kwargs):
#         queryset = super().get_queryset(*args, **kwargs)
#         queryset = queryset.filter(type=User.Types.PATIENT)
#         return queryset


# class PatientAdditional(models.Model):

#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name='patient')


# class Patient(User):
#     class Meta:
#         proxy = True
#     objects = PatientManager()

#     @property
#     def showAdditional(self):
#         return self.PatientAdditional

#     def save(self, *args, **kwargs):
#         self.type = User.Types.PATIENT
#         self.is_patient = True
#         return super().save(*args, **kwargs)

#     def __str__(self):
#         return f'{self.user.first_name} {self.user.last_name}@patient'
