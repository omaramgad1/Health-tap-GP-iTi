from rest_framework import serializers
from Reservation.models import Reservation
from Patient.api.serializers import PatientSerializer


class Reservation_Appointment_Serializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ["patient"]


class ReservationSerializer(serializers.ModelSerializer):
    appointment_time = serializers.SerializerMethodField()
    appointment_duration = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    appointment_price = serializers.SerializerMethodField()

    def get_appointment_time(self, obj):
        # Format the time with AM/PM designation
        time = obj.appointment.start_time.strftime("%I:%M %p")
        return time.upper()  # Format the time as desired

    def get_appointment_duration(self, obj):
        return obj.appointment.duration

    def get_appointment_date(self, obj):
        return obj.appointment.date

    def get_appointment_price(self, obj):
        return obj.appointment.price

    class Meta:
        model = Reservation
        fields = '__all__'
