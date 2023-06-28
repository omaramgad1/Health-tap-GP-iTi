from ..models import Appointment, Doctor
from rest_framework import serializers


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(
        source='doctor.user.first_name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor', 'date', 'start_time', 'duration', 'price', 'status',
            'end_time'
        ]
        read_only_fields = ['id', 'end_time']
