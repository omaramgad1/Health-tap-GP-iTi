from cloudinary.models import CloudinaryField, CloudinaryResource
import cloudinary.api
from django.core.exceptions import ValidationError
from django.db import models
from Patient.models import Patient
from Doctor.models import Doctor
from Appointment.models import Appointment


def validateImage(image):
    if not isinstance(image, CloudinaryResource):
        # The image is not a Cloudinary resource, so we can't validate it
        return

    info = cloudinary.api.resource(image.public_id)
    file_size = info.get("bytes")
    if not file_size:
        raise ValidationError('Failed to get image size.')

    print(file_size)
    if file_size > 2 * 1024 * 1024:
        raise ValidationError('Image size should be less than 2MB.')

    file_extension = image.format.lower()
    if file_extension not in ['png', 'jpg', 'jpeg']:
        raise ValidationError('Only PNG, JPG, and JPEG images are allowed.')


class MedicalEntry(models.Model):
    comment = models.TextField()
    prescription = models.TextField(null=True, blank=True)
    analysis_image = CloudinaryField(
        null=True, blank=True, validators=[validateImage])
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='medical_history')
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Medical Entry for {self.patient}'
