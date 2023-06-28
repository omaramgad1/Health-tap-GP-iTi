from rest_framework import generics
from rest_framework.decorators  import  api_view, permission_classes
from rest_framework.response import Response
from Appointment.models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.permissions import IsAuthenticated

# class AppointmentView(generics.ListCreateAPIView):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer(queryset)

@api_view()
@permission_classes([IsAuthenticated])
def appointment_list(request):
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(queryset=appointments)
    return Response(serializer)

@api_view()
@permission_classes([IsAuthenticated])
def appointment_detailes(request, id):
    appointment = Appointment.objects.get(pk=id)
    serializer = AppointmentSerializer(appointment)
    return Response(serializer)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])

def add_appointment(request):
    pass