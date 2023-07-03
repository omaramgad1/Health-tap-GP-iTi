from MedicalEntry.pagination import EntriesPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import MedicalEntry
from .serializers import MedicalEntrySerializer
from Patient.models import Patient
from rest_framework import status, generics
from django.db import transaction
from MedicalCode.models import MedicalEditCode
from Appointment.models import Appointment
from rest_framework import generics, filters
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.core.paginator import Paginator
from Health_tap_Backend.permissions import IsDoctor, IsPatient


@api_view(['GET'])
@permission_classes([IsPatient])
def patient_medical_entry_list(request):
    # Get the currently authenticated user (assumed to be a Patient)
    patient = request.user.patient

    # Get the MedicalEntry objects for this patient
    base_url = request.scheme + '://' + request.get_host()

    queryset = MedicalEntry.objects.filter(
        patient=patient).order_by('created_at')
    queryset_len = MedicalEntry.objects.filter(
        patient=patient).order_by('created_at').count()
    size = request.GET.get('size', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, size)
    objects = paginator.get_page(page)
    serializer = MedicalEntrySerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/patient/list/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}patient/list/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,

                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })


@api_view(['GET'])
@permission_classes([IsDoctor])
def patient_medical_entry_list_doctor(request, patient_id, appointment_id):
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    edit = False
    try:

        MedicalEntry.objects.get(
            patient=patient,  appointment=appointment)
        edit = False

    except MedicalEntry.DoesNotExist:
        edit = True

    # Get the MedicalEntry objects for this patient
    base_url = request.scheme + '://' + request.get_host()

    queryset = MedicalEntry.objects.filter(
        patient=patient).order_by('created_at')
    queryset_len = MedicalEntry.objects.filter(
        patient=patient).order_by('created_at').count()
    # limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)
    objects = paginator.get_page(page)
    serializer = MedicalEntrySerializer(objects, many=True)

    return Response({'result': serializer.data,
                     'next': f'{base_url}/doctor/patient/list/{patient_id}/?page={objects.next_page_number()}' if objects.has_next() else None,
                     'previous': f'{base_url}/doctor/patient/list/{patient_id}/?page={objects.previous_page_number()}' if objects.has_previous() else None,
                     'count': queryset_len,
                     "edit": edit,
                     'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                     'current_page': objects.number,
                     'next_page': objects.next_page_number() if objects.has_next() else None,
                     'total_pages': paginator.num_pages,
                     })


@api_view(['POST'])
@permission_classes([IsDoctor])
def medical_entry_create(request, patient_id, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        print(appointment.doctor)

        if request.user.doctor != appointment.doctor:
            return Response({'error': "Invaild Appointment id"}, status=status.HTTP_401_UNAUTHORIZED)

        patient = Patient.objects.get(id=patient_id)
        try:
            MedicalEntry.objects.get(
                patient=patient, appointment=appointment)
            return Response({'error': "You Can not add another Entry at this appointment you Can edit the old one"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except MedicalEntry.DoesNotExist:
            pass
        # Get the patient object from the request data
        if not request.data.get('code'):
            return Response({'error': "Medical Edit Code is Required"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            # Get the medical edit code from the request data
        medical_edit_code = MedicalEditCode.objects.get(
            patient=patient, appointment=appointment, code=request.data.get('code'))

        # Check if the medical edit code is valid
        if not medical_edit_code.is_valid():
            return Response({'message': 'The medical edit code is expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)

        req_data = {
            'comment': request.data.get('comment'),
            'prescription': request.data.get('prescription') if request.data.get('prescription') else None,
            'analysis_image': request.data.get('analysis_image') if request.data.get('analysis_image') else None,
        }

        # Create a new MedicalEntry object
        serializer = MedicalEntrySerializer(data=req_data)
        if serializer.is_valid():
            # Save the new MedicalEntry object
            with transaction.atomic():
                # Save the new MedicalEntry object
                serializer.save(
                    doctor=request.user.doctor, patient=patient, appointment=appointment)

            # Return the serialized data for the new object
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    except MedicalEditCode.DoesNotExist:
        return Response({'error': 'Medical Edit Code not found'}, status=status.HTTP_404_NOT_FOUND)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsDoctor])
def medical_entry_update(request, medical_entry_id, patient_id, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if request.user.doctor != appointment.doctor:
            return Response({'error': "Invaild Appointment id"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the patient object from the request data
        patient = Patient.objects.get(id=patient_id)

        if not request.data.get('code'):
            return Response({'error': "Medical Edit Code is Required"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Get the medical edit code from the request data
        medical_edit_code = MedicalEditCode.objects.get(
            patient=patient, appointment=appointment, code=request.data.get('code'))

        # Check if the medical edit code is valid
        if not medical_edit_code.is_valid():
            return Response({'message': 'The medical edit code is expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the MedicalEntry object to update
        medical_entry = MedicalEntry.objects.get(id=medical_entry_id)

        if request.user.doctor != medical_entry.doctor:
            return Response({'message': 'You are not authorized to update this medical entry'}, status=status.HTTP_403_FORBIDDEN)
        if appointment != medical_entry.appointment:
            return Response({'message': 'You can not update this medical entry'}, status=status.HTTP_403_FORBIDDEN)

        req_data = {
            'comment': request.data.get('comment') if request.data.get('comment') else medical_entry.comment,
            'prescription': request.data.get('prescription') if request.data.get('prescription') else medical_entry.prescription,
            'analysis_image': request.data.get('analysis_image') if request.data.get('analysis_image') else medical_entry.analysis_image,
        }

        serializer = MedicalEntrySerializer(medical_entry, data=req_data)
        if serializer.is_valid():
            # Save the updated MedicalEntry object
            with transaction.atomic():
                serializer.save()
                # Set the medical edit code status to 'expired'

                # Return the serialized data for the updated object
                return Response(serializer.data, status=status.HTTP_200_OK)

    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    except MedicalEditCode.DoesNotExist:
        return Response({'error': 'Medical Edit Code not found'}, status=status.HTTP_404_NOT_FOUND)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


class PatientMedicalEntryList(generics.ListAPIView):
    serializer_class = MedicalEntrySerializer
    pagination_class = EntriesPagination
    filter_backends = [DjangoFilterBackend]
    search_fields = ['doctor__specialization__name', 'doctor__id']

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        queryset = MedicalEntry.objects.filter(
            patient=patient).order_by('-created_at')

        specialization_term = self.request.query_params.get('specialization')
        if specialization_term:
            queryset = queryset.filter(
                doctor__specialization=specialization_term)

        doctor_id_term = self.request.query_params.get('doctor_id')
        if doctor_id_term:
            queryset = queryset.filter(doctor__id=doctor_id_term)

        return queryset
