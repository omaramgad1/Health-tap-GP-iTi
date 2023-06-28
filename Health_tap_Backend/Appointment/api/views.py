from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Appointment, Doctor
from .serializers import AppointmentSerializer
from django.utils import timezone

############################## Doctor #####################


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_appointment(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    serializer = AppointmentSerializer(
        data=request.data, context={'doctor': doctor})
    if serializer.is_valid():
        appointment = serializer.save(doctor=doctor)
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_doctor_appointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = doctor.appointments.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_all_appointments(request):
#     appointments = Appointment.objects.all()
#     serializer = AppointmentSerializer(appointments, many=True)
#     return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_appointment(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointment = get_object_or_404(
        Appointment, id=appointment_id, doctor=doctor)
    serializer = AppointmentSerializer(
        appointment, data=request.data, partial=True)
    if serializer.is_valid():
        appointment = serializer.save()
        return Response(AppointmentSerializer(appointment).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_appointment(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointment = get_object_or_404(
        Appointment, id=appointment_id, doctor=doctor)
    if appointment.status == 'A':
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Cannot delete a reserved appointment.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_available_appointments(request):
    today = timezone.localdate()
    max_date = today + timezone.timedelta(days=6)
    appointments = Appointment.objects.filter(
        date__range=[today, max_date], status='A')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_reserved_appointments(request):
    today = timezone.localdate()
    max_date = today + timezone.timedelta(days=6)
    appointments = Appointment.objects.filter(
        date__range=[today, max_date], status='R')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)
