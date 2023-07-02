from ..models import Appointment, Doctor
from rest_framework import serializers
from datetime import datetime, timedelta, time
from django.utils import timezone
from Reservation.api.serializers import Reservation_Appointment_Serializer
from Reservation.models import Reservation


class AppointmentSerializer(serializers.ModelSerializer):
    # doctor = serializers.CharField(
    #     source='doctor.first_name', read_only=True)
    reservation_data = Reservation_Appointment_Serializer(
        read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor', 'date', 'start_time', 'duration', 'price', 'status',
            'end_time', 'reservation_data'
        ]
        read_only_fields = ['id', 'end_time', 'doctor']

    def validate(self, data):
        # Get the `doctor` object from the context
        doctor = self.context['doctor']

        # Call the superclass's `validate` method to get the validated data
        data = super().validate(data)

        # Add the `doctor` object to the validated data
        data['doctor'] = doctor

        # Check for overlapping appointments
        start_time = data['start_time']
        duration = data['duration']
        end_time = (datetime.combine(data['date'], start_time) +
                    timedelta(minutes=duration)).time()

        overlapping_appointments = Appointment.objects.filter(
            doctor=doctor,
            date=data['date'],
            start_time__lt=end_time,
        ).exclude(id=self.instance.id if self.instance else None)

        for appointment in overlapping_appointments:
            if appointment.end_time() > start_time:
                raise serializers.ValidationError({
                    'error': 'This appointment overlaps with another appointment.'})

        return data
