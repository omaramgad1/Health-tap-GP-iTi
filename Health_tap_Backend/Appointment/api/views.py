from django.shortcuts import get_object_or_404
import pytz
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Appointment, Doctor
from .serializers import AppointmentSerializer
from django.utils import timezone
from datetime import datetime, timedelta, time

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
    now = timezone.localtime()
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    current_date = now.date()
    appointments = doctor.appointments.filter(date__gte=current_date)

    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_doctor_history_appointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    now = timezone.localtime()
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    appointments = doctor.appointments.filter(date__lt=now.date())

    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_appointment(request, appointment_id):
    # Get the `doctor` object from the request user
    doctor = get_object_or_404(Doctor, user=request.user)

    # Get the `appointment` object for the given ID and doctor
    appointment = get_object_or_404(
        Appointment, id=appointment_id, doctor=doctor)

    # Initialize the serializer with the `appointment` object and request data,
    # and pass the `doctor` object to the serializer's `context`
    serializer = AppointmentSerializer(
        appointment, data=request.data, partial=True,
        context={'doctor': doctor})

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
        return Response({'message': 'Appointment Deleted Successfuly'}, status=status.HTTP_200_OK)
    return Response({'error': 'Cannot delete a reserved appointment.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_available_appointments(request):
    now = timezone.localtime()
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    today = now.date()
    max_date = today + timezone.timedelta(days=6)
    appointments = Appointment.objects.filter(
        date__range=[today, max_date], status='A')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_reserved_appointments(request):
    now = timezone.localtime()
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    today = now.date()
    max_date = today + timezone.timedelta(days=6)
    appointments = Appointment.objects.filter(
        date__range=[today, max_date], status='R')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_appointments(request):
    # Get the `doctor` object from the request user
    doctor = get_object_or_404(Doctor, user=request.user)
    # Get the current date and time in the server's timezone
    now = timezone.localtime()
    # Convert the current date and time to the doctor's timezone
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)

    # Get the appointments for today that are not already booked
    available_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=now.date(),
        status='A',
    )
    # Serialize the available appointments and return the response
    serializer = AppointmentSerializer(available_appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reserved_appointments(request):
    # Get the `doctor` object from the request user
    doctor = get_object_or_404(Doctor, user=request.user)

    # Get the current date and time in the server's timezone
    now = timezone.localtime()

    # Convert the current date and time to the doctor's timezone
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)

    # Get the appointments for today that are not already booked
    available_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=now.date(),
        status='R',
    )
    # Serialize the available appointments and return the response
    serializer = AppointmentSerializer(available_appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def count_available_reserved_appointments(request):
    today = timezone.localdate()
    max_date = today + timezone.timedelta(days=6)
    count_T_A = Appointment.objects.filter(
        date=today, status='A').count()
    count_T_R = Appointment.objects.filter(
        date=today, status='R').count()
    count_A = Appointment.objects.filter(
        date__range=[today, max_date], status='A').count()

    count_R = Appointment.objects.filter(
        date__range=[today, max_date], status='R').count()

    return Response({'today_A': count_T_A, 'today_R': count_T_R, "Available": count_A, "Reserved": count_R, 'total': count_A+count_R}, status=status.HTTP_200_OK)
