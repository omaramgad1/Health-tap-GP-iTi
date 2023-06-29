
from rest_framework import serializers
from ..models import Doctor


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone', 'national_id', 'profileImgUrl',
                  'password', 'confirm_password', 'gender', 'specialization', 'profLicenseNo', 'city', 'district', 'address']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        del validated_data['confirm_password']
        doctor = Doctor.objects.create_doctor(**validated_data)
        return doctor

