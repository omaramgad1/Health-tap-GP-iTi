from rest_framework import serializers
from ..models import MedicalEntry
from Doctor.api.serializers import DoctorSerializer
from Patient.api.serializers import PatientSerializer


class MedicalEntrySerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = MedicalEntry
        fields = ['id', 'comment', 'prescription_image', 'analysis_image',
                  'patient', 'doctor', 'created_at', 'updated_at']
