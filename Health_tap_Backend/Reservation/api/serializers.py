from rest_framework import serializers
from Reservation.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    appointment_time = serializers.SerializerMethodField()
    appointment_duration = serializers.SerializerMethodField()
    appointment_date = serializers.SerializerMethodField()
    appointment_price = serializers.SerializerMethodField()

    def get_appointment_time(self, obj):
        time = obj.appointment.start_time.strftime("%I:%M %p")  # Format the time with AM/PM designation
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
