from User.models import Patient, Doctor, User
from Specialization.api.serializers import SpecializationSerializer
from Specialization.models import Specialization
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from City.models import City
from District.models import District
from Appointment.api.serializers import AppointmentSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'gender', 'password', 'confirm_password',
                  'email', 'date_of_birth', 'phone', 'national_id',  'created', 'updated']
# 'profileImgUrl',

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError('This email is already exists!')

        if 'phone' not in data:
            raise serializers.ValidationError('Phone number is required.')

        if User.objects.filter(phone=data['phone']).exists():
            raise serializers.ValidationError('Phone number already exists.')

        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords don't match")

        if len(data['password']) > 16 or len(data['confirm_password']) > 16:
            raise ValidationError(
                "Password should not be more than 16 characters")

        return data


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
    city_id = serializers.IntegerField(write_only=True)
    district_id = serializers.IntegerField(write_only=True)
    appointments = AppointmentSerializer(
        many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization',
                  'profLicenseNo', 'city_id', 'district_id', 'appointments']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        specialization_data = validated_data.pop('specialization')
        specialization_name = specialization_data.get('name')
        city_id = validated_data.pop('city_id')
        district_id = validated_data.pop('district_id')

        with transaction.atomic():
            try:
                specialization = Specialization.objects.get(
                    name=specialization_name)
            except Specialization.DoesNotExist:
                raise serializers.ValidationError(
                    f'Specialization "{specialization_name}" does not exist')

            try:
                city = City.objects.get(id=city_id)
            except City.DoesNotExist:
                raise serializers.ValidationError(
                    f'City with id "{city_id}" does not exist')

            try:
                district = District.objects.get(id=district_id, city=city)
            except District.DoesNotExist:
                raise serializers.ValidationError(
                    f'District with id "{district_id}" does not exist in the given city')

            user = User.objects.create(**user_data)
            doctor = Doctor.objects.create(
                user=user, specialization=specialization, city=city, district=district, **validated_data)

        return doctor


# from django.contrib.auth import get_user_model
# from ..models import User


# class UserSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(
#         style={'input_type': 'password'}, write_only=True)

#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'first_name', 'last_name', 'phone', 'gender',
#                   'national_id', 'date_of_birth', 'password', 'password2']
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     # Validating Password and Confirm Password while Registration

#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         if password != password2:
#             raise serializers.ValidationError(
#                 "Password and Confirm Password doesn't match")
#             # Custom password validation
#         if len(password) < 8:
#             raise serializers.ValidationError(
#                 {"password": "Password must be at least 8 characters long."})

#         if password.isnumeric():
#             raise serializers.ValidationError(
#                 {"password": "Password cannot contain only numeric characters."})

#         return attrs

#     def create(self, validate_data):
#         return User.objects.create_user(**validate_data)
