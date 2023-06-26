from rest_framework import serializers
from User.models import Patient, Doctor, User
from Specialization.api.serializers import SpecializationSerializer
from Specialization.models import Specialization
from django.db import transaction
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',  'password' , 'confirm_password' ,'email', 'date_of_birth', 'phone', 'national_id', 'profileImgUrl', 'created', 'updated']


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient
    
class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    specialization = SpecializationSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'profLicenseNo']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        specialization_data = validated_data.pop('specialization')
        specialization_name = specialization_data.get('name')

        with transaction.atomic():
            try:
                specialization = Specialization.objects.get(name=specialization_name)
            except Specialization.DoesNotExist:
                raise serializers.ValidationError(f'Specialization "{specialization_name}" does not exist')

            user = User.objects.create(**user_data)
            doctor = Doctor.objects.create(user=user, specialization=specialization, **validated_data)

        return doctor