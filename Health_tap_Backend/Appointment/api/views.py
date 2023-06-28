from rest_framework import generics
from Appointment.models import Appointment
from .serializers import AppointmentSerializer

class AppointmentView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
