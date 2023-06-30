from rest_framework import serializers
from Review.models import Review
from Patient.models import Patient
from Doctor.models import Doctor


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name']  


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name']  


class ReviewSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rate', 'comment', 'patient', 'doctor']
