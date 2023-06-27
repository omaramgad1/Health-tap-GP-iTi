from rest_framework import serializers
from django.contrib.auth import get_user_model
from User.api.serializers import UserSerializer
from ..models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'specialization', 'profLicenseNo']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(is_doctor=True)
            doctor = Doctor.objects.create(user=user, **validated_data)
            return doctor
