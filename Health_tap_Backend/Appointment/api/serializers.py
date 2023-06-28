from ..models import Appointment, Doctor
from rest_framework import serializers
from datetime import datetime, timedelta, time
from django.utils import timezone


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(
        source='doctor.user.first_name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor', 'date', 'start_time', 'duration', 'price', 'status',
            'end_time'
        ]
        read_only_fields = ['id', 'end_time', 'doctor']

    def validate(self, data):
        # Get the `doctor` object from the context
        doctor = self.context['doctor']

        validated_data = super().validate(data)

        # Add the `doctor` object to the validated data
        validated_data['doctor'] = doctor

        # Check for overlapping appointments
        start_time = validated_data['start_time']
        duration = validated_data['duration']
        end_time = (datetime.combine(validated_data['date'], start_time) +
                    timedelta(minutes=duration)).time()

        print(start_time)
        print(end_time)
        overlapping_appointments = Appointment.objects.filter(
            doctor=doctor,
            date=validated_data['date'],
            start_time__lt=end_time,
            # end_time__gt=start_time,
        ).exclude(id=validated_data.get('id'))

        print(overlapping_appointments)

        for appointment in overlapping_appointments:
            print(appointment.end_time())
            # Do something with `appointment`
            print(appointment.date, appointment.start_time, appointment.duration)
            if overlapping_appointments.exists() and appointment.end_time() > start_time:
                raise serializers.ValidationError(
                    'This appointment overlaps with another appointment.')

        return validated_data
