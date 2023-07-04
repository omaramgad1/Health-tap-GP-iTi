from django.shortcuts import get_object_or_404
import pytz
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Appointment, Doctor
from .serializers import AppointmentSerializer
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.core.paginator import Paginator
from Health_tap_Backend.permissions import IsDoctor
############################## Doctor #####################


@api_view(['POST'])
@permission_classes([IsDoctor])
def add_appointment(request):

    doctor = request.user.doctor
    serializer = AppointmentSerializer(
        data=request.data, context={'doctor': doctor})
    if serializer.is_valid():
        appointment = serializer.save(doctor=doctor)
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsDoctor])
def list_doctor_appointments(request):

    doctor = request.user.doctor
    now = timezone.localtime()
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    current_date = now.date()

    base_url = request.scheme + '://' + request.get_host()

    queryset = doctor.appointments.filter(
        date__gte=current_date).order_by('date', 'start_time')
    queryset_len = doctor.appointments.filter(date__gte=current_date).count()
    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = AppointmentSerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/appointment/doctor/list-all/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/appointment/doctor/list-all/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })


@api_view(['GET'])
@permission_classes([IsDoctor])
def list_doctor_history_appointments(request):
    doctor = request.user.doctor
    now = timezone.localtime()
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    base_url = request.scheme + '://' + request.get_host()

    queryset = doctor.appointments.filter(date__lt=now.date())
    queryset_len = doctor.appointments.filter(date__lt=now.date()).count()
    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = AppointmentSerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/appointment/doctor/list-history/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/appointment/doctor/list-history/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })


@api_view(['PUT'])
@permission_classes([IsDoctor])
def edit_appointment(request, appointment_id):
    # Get the `doctor` object from the request user

    doctor = request.user.doctor

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
@permission_classes([IsDoctor])
def delete_appointment(request, appointment_id):

    doctor = request.user.doctor
    appointment = get_object_or_404(
        Appointment, id=appointment_id, doctor=doctor)
    if appointment.status == 'A':
        appointment.delete()
        return Response({'message': 'Appointment Deleted Successfuly'}, status=status.HTTP_200_OK)
    return Response({'error': 'Cannot delete a reserved appointment.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsDoctor])
def list_available_appointments(request):

    now = timezone.localtime()
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    today = now.date()
    max_date = today + timezone.timedelta(days=7)

    base_url = request.scheme + '://' + request.get_host()

    queryset = Appointment.objects.filter(
        doctor=request.user.doctor,
        date__range=[today, max_date], status='A').order_by('date', 'start_time')
    queryset_len = Appointment.objects.filter(
        doctor=request.user.doctor,
        date__range=[today, max_date], status='A').count()

    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = AppointmentSerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/appointment/doctor/list/available/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/appointment/doctor/list/available/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })


@api_view(['GET'])
@permission_classes([IsDoctor])
def list_reserved_appointments(request):

    now = timezone.localtime()
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    today = now.date()
    max_date = today + timezone.timedelta(days=7)
    base_url = request.scheme + '://' + request.get_host()

    queryset = Appointment.objects.filter(
        doctor=request.user.doctor,
        date__range=[today, max_date], status='R').order_by('date', 'start_time')
    queryset_len = Appointment.objects.filter(
        date__range=[today, max_date], status='R').count()
    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = AppointmentSerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/appointment/doctor/list-all/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/appointment/doctor/list-all/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })


@api_view(['GET'])
@permission_classes([IsDoctor])
def get_available_appointments(request):
    # Get the `doctor` object from the request user
    doctor = request.user.doctor
    # Get the current date and time in the server's timezone
    now = timezone.localtime()
    # Convert the current date and time to the doctor's timezone
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)

    # Get the appointments for today that are not already booked
    base_url = request.scheme + '://' + request.get_host()

    queryset = Appointment.objects.filter(
        doctor=doctor,
        date=now.date(),
        status='A',
    ).order_by('date', 'start_time')
    queryset_len = Appointment.objects.filter(
        doctor=doctor,
        date=now.date(),
        status='A',
    ).count()
    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = AppointmentSerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/appointment/doctor/list/today/available/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/appointment/doctor/list/today/available/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })


@api_view(['GET'])
@permission_classes([IsDoctor])
def get_reserved_appointments(request):
    # Get the `doctor` object from the request user

    doctor = request.user.doctor

    # Get the current date and time in the server's timezone
    now = timezone.localtime()

    # Convert the current date and time to the doctor's timezone
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)

    # Get the appointments for today that are not already booked
    base_url = request.scheme + '://' + request.get_host()

    queryset = Appointment.objects.filter(
        doctor=doctor,
        date=now.date(),
        status='R',
    ).order_by('date', 'start_time')
    queryset_len = Appointment.objects.filter(
        doctor=doctor,
        date=now.date(),
        status='R',
    ).count()
    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = AppointmentSerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/appointment/doctor/list/reserved/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/appointment/doctor/list/reserved/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })


@api_view(['GET'])
@permission_classes([IsDoctor])
def count_available_reserved_appointments(request):

    now = timezone.localtime()
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    today = now.date()
    max_date = today + timezone.timedelta(days=7)

    count_T_A = Appointment.objects.filter(
        doctor=request.user.doctor,
        date=today, status='A').count()

    count_T_R = Appointment.objects.filter(
        doctor=request.user.doctor,
        date=today, status='R').count()

    count_A = Appointment.objects.filter(
        doctor=request.user.doctor,
        date__range=[today, max_date], status='A').count()

    count_R = Appointment.objects.filter(
        doctor=request.user.doctor,
        date__range=[today, max_date], status='R').count()

    return Response({'today_A': count_T_A, 'today_R': count_T_R, "Available": count_A, "Reserved": count_R, 'total': count_A+count_R}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsDoctor])
def list_doctor_appointments_by_date(request, date):

    doctor = request.user.doctor

    base_url = request.scheme + '://' + request.get_host()

    queryset = Appointment.objects.filter(
        doctor=doctor,
        date=date
    ).order_by('start_time')
    queryset_len = Appointment.objects.filter(
        doctor=doctor,
        date=date.trim()
    ).count()

    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = AppointmentSerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/appointment/doctor/list/date/{date.trim()}/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/appointment/doctor/list/date/{date.trim()}/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })

############################## Patient #####################


@api_view(['GET'])
@permission_classes([AllowAny])
def get_available_appointments_patient(request, doctor_id):

    # Get the `doctor` object from the request user
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get the current date and time in the server's timezone
    now = timezone.localtime()
    # Convert the current date and time to the doctor's timezone
    tz = pytz.timezone('Africa/Cairo')
    now = now.astimezone(tz)
    today = now.date()
    max_date = today + timezone.timedelta(days=7)
    # Get the appointments for today that are not already booked
    base_url = request.scheme + '://' + request.get_host()

    queryset = Appointment.objects.filter(
        doctor=doctor,
        date__range=[today, max_date], status='A'
    ).order_by('date', 'start_time')
    queryset_len = Appointment.objects.filter(
        doctor=doctor,
        date__range=[today, max_date], status='A'
    ).count()
    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = AppointmentSerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/appointment/patient/doctor/{doctor_id}/available/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/appointment/patient/doctor/{doctor_id}/available/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })


@api_view(['GET'])
@permission_classes([AllowAny])
def list_doctor_appointments_by_date_pateint(request, doctor_id, date):
    # Get the `doctor` object from the request user
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    base_url = request.scheme + '://' + request.get_host()

    queryset = Appointment.objects.filter(
        doctor=doctor,
        date=date
    ).order_by('start_time')
    queryset_len = Appointment.objects.filter(
        doctor=doctor,
        date=date
    ).count()

    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = AppointmentSerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/appointment/doctor/list/date/{date}/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/appointment/doctor/list/date/{date}/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })
