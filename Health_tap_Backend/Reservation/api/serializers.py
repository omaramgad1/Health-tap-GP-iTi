from rest_framework import serializers
from Reservation.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reservation
        fields = '__all__'

