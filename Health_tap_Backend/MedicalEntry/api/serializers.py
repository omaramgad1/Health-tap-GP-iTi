from rest_framework import serializers
from ..models import MedicalEntry
from Doctor.api.serializers import DoctorSerializer
from Patient.api.serializers import PatientSerializer
from Appointment.api.serializers import AppointmentSerializer


class MedicalEntrySerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = MedicalEntry
        fields = ['id', 'comment', 'prescription', 'analysis_image', 'created_at', 'updated_at',
                  'patient', 'doctor', 'appointment']
