from rest_framework import serializers
from Reservation.models import Reservation
from Patient.api.serializers import PatientSerializer


class Reservation_Appointment_Serializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ["patient"]


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = '__all__'
