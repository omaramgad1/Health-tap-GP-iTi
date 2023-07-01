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


class MedicalEditCodeListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalEditCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'patient'):
            return MedicalEditCode.objects.filter(patient=self.request.user.patient)
        return MedicalEditCode.objects.none()

    def post(self, request, *args, **kwargs):
        if not hasattr(request.user, 'patient'):
            return Response({'detail': 'You are not authorized to create a medical edit code.'}, status=status.HTTP_400_BAD_REQUEST)

        patient = request.user.patient
        # patient = get_object_or_404(Patient, id=patient_id)
        appointment_id = self.kwargs['appointment_id']

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        medical_edit_code = MedicalEditCode.objects.get(
            patient=patient, appointment=appointment)

        if medical_edit_code:
            MedicalEditCode.objects.filter(
                patient=patient).exclude(patient=patient, appointment=appointment).delete()

            serializer = self.get_serializer(medical_edit_code)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:

            MedicalEditCode.objects.filter(
                patient=patient).delete()
            import random
            import string
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

            medical_edit_code = MedicalEditCode.objects.create(
                **validated_data)

        serializer = self.get_serializer(medical_edit_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MedicalEditCodeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalEditCode.objects.all()
    serializer_class = MedicalEditCodeSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == 'V':
            instance.status = 'E'
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'detail': 'Cannot delete an expired medical edit code'}, status=status.HTTP_400_BAD_REQUEST)


class PatientMedicalEntryListDoctorView(generics.GenericAPIView):
    serializer_class = MedicalEntrySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor = request.user.doctor
        if not doctor or not doctor.is_doctor:
            return Response({'detail': 'You are not authorized to perform this operation.'}, status=status.HTTP_403_FORBIDDEN)

        patient_id = self.kwargs['patient_id']
        patient = get_object_or_404(Patient, id=patient_id)

        medical_edit_code = MedicalEditCode.objects.filter(
            patient=patient).first()
        if not medical_edit_code:
            return Response({'detail': 'Invalid medical edit code.'}, status=status.HTTP_400_BAD_REQUEST)

        if medical_edit_code.status == 'E' or dt.now().date() > medical_edit_code.expired_at.date():
            return Response({'detail': 'Medical edit code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        base_url = request.scheme + '://' + request.get_host()
        return redirect(f'{base_url}/medical-entry/doctor/patient/list/{patient_id}/')
