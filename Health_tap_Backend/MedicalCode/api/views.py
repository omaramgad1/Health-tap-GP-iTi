from MedicalEntry.models import MedicalEntry
from MedicalEntry.api.serializers import MedicalEntrySerializer
from rest_framework import generics, status
from rest_framework.response import Response
from Patient.models import Patient
from rest_framework.permissions import IsAuthenticated
from MedicalCode.models import MedicalEditCode
from MedicalCode.api.serializers import MedicalEditCodeSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from Doctor.models import Doctor
from datetime import datetime as dt
from Appointment.models import Appointment
from django.db import IntegrityError
import random
import string
from Health_tap_Backend.permissions import IsDoctor, IsPatient


class MedicalEditCodeListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalEditCodeSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        print("query set")
        if hasattr(self.request.user, 'patient'):
            print(self.request.user.patient)
            return MedicalEditCode.objects.filter(patient=self.request.user.patient)
        return MedicalEditCode.objects.none()

    def post(self, request, *args, **kwargs):
        # if not hasattr(request.user, 'patient'):
        #     return Response({'detail': 'You are not authorized to create a medical edit code.'}, status=status.HTTP_400_BAD_REQUEST)

        patient = request.user.patient
        appointment_id = self.kwargs['appointment_id']
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            if appointment.status != 'R':
                return Response({'detail': 'The appointment is not reserved.'}, status=status.HTTP_400_BAD_REQUEST)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        # if appointment.start_time is not timezone.now():
        #     return Response({'error': 'Appointment is not started'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            medical_edit_code = MedicalEditCode.objects.get(
                patient=patient, appointment=appointment)
            MedicalEditCode.objects.filter(
                patient=patient).exclude(patient=patient, appointment=appointment).delete()
            serializer = self.get_serializer(medical_edit_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MedicalEditCode.DoesNotExist:
            MedicalEditCode.objects.filter(
                patient=patient).delete()

            code = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))

            validated_data = {
                'patient': patient,
                'appointment': appointment,
                'code': code,
                'created_at': timezone.now(),
                'expired_at': timezone.now() + timezone.timedelta(hours=1),
                'status': 'V',
            }

        try:
            medical_edit_code = MedicalEditCode.objects.create(
                **validated_data)
        except IntegrityError:
            return Response({'detail': 'This Appointment already have a medical code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(medical_edit_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MedicalEditCodeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalEditCode.objects.all()
    serializer_class = MedicalEditCodeSerializer
    permission_classes = [IsPatient]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == 'V':
            instance.status = 'E'
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'detail': 'Cannot delete an expired medical edit code'}, status=status.HTTP_400_BAD_REQUEST)


class PatientMedicalEntryListDoctorView(generics.GenericAPIView):
    serializer_class = MedicalEntrySerializer
    permission_classes = [IsDoctor]

    def post(self, request, appointment_id, *args, **kwargs):
        doctor = request.user.doctor
        if not doctor or not doctor.is_doctor:
            return Response({'detail': 'You are not authorized to perform this operation.'}, status=status.HTTP_403_FORBIDDEN)

        patient_id = self.kwargs['patient_id']
        patient = get_object_or_404(Patient, id=patient_id)
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            if appointment.status != 'R':
                return Response({'detail': 'The appointment is not reserved.'}, status=status.HTTP_400_BAD_REQUEST)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.data.get('code'):
            return Response({'error': "Medical Edit Code is Required"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        medical_edit_code = MedicalEditCode.objects.filter(
            patient=patient, appointment=appointment, code=request.data.get('code')).first()
        if not medical_edit_code:
            return Response({'detail': 'Invalid medical edit code.'}, status=status.HTTP_400_BAD_REQUEST)

        appointment = get_object_or_404(Appointment, id=appointment_id)
        if appointment != medical_edit_code.appointment or appointment.status != 'R':
            return Response({'detail': 'Invalid appointment or the appointment is not completed.'}, status=status.HTTP_400_BAD_REQUEST)

        if medical_edit_code.status == 'E' or dt.now().date() > medical_edit_code.expired_at.date():
            return Response({'detail': 'Medical edit code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        base_url = request.scheme + '://' + request.get_host()
        return redirect(f'{base_url}/medical-entry/doctor/patient/list/{patient_id}/')
