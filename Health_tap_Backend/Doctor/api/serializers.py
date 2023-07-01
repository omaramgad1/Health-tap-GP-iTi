
from rest_framework import serializers
from ..models import Doctor
import re
from django.core.exceptions import ValidationError


class DoctorSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(
        source='specialization.name', read_only=True)
    city = serializers.CharField(
        source='city.name_en', read_only=True)
    district = serializers.CharField(
        source='district.name_en', read_only=True)

    class Meta:
        model = Doctor
        # fields = '__all__'
        exclude = ["password",
                   "confirm_password",
                   "created",
                   "updated",
                   "is_staff",
                   "is_active",
                   "is_superuser",
                   "is_doctor",
                   "groups",
                   "user_permissions", "last_login"]


def validate_profLicenseNum(value):
    pattern = r'^[02468]\d[13579]{2}\d{2}$'
    match = re.match(pattern, value)
    if match is None:
        raise ValidationError("profession License Number Invalid!.")


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone', 'national_id', 'profileImgUrl',
                  'password', 'confirm_password', 'gender', 'specialization', 'profLicenseNo', 'city', 'district', 'address']

    def validate(self, data):

        try:
            validate_profLicenseNum(data['profLicenseNo'])
        except ValidationError as error:
            raise serializers.ValidationError(str(error))

        if len(data['password']) < 8:
            raise serializers.ValidationError(
                'Password must be at least 8 characters long')
        if not any(c.isdigit() for c in data['password']):
            raise serializers.ValidationError(
                'Password must contain at least one digit')

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        del validated_data['confirm_password']
        doctor = Doctor.objects.create_doctor(**validated_data)
        return doctor
