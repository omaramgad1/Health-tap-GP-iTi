from MedicalEntry.models import MedicalEntry
from MedicalEntry.api.serializers import MedicalEntrySerializer
from rest_framework import generics, status
from rest_framework.response import Response
from Patient.models import Patient
from rest_framework.permissions import IsAuthenticated
from MedicalCode.models import MedicalEditCode
from MedicalCode.api.serializers import MedicalEditCodeSerializer
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from Doctor.models import Doctor
from datetime import datetime as dt
from django.urls import reverse


class MedicalEditCodeListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalEditCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("query set")
        if hasattr(self.request.user, 'patient'):
            print(self.request.user.patient)
            return MedicalEditCode.objects.filter(patient=self.request.user.patient)
        return MedicalEditCode.objects.none()

    def post(self, request, *args, **kwargs):
        if not hasattr(request.user, 'patient'):
            return Response({'detail': 'You are not authorized to create a medical edit code.'}, status=status.HTTP_400_BAD_REQUEST)

        patient_id = request.user.patient.id
        patient = get_object_or_404(Patient, id=patient_id)

        medical_edit_code = MedicalEditCode.objects.filter(
            patient=patient, status='V').first()
        if medical_edit_code:
            medical_edit_code.created_at = timezone.now()
            medical_edit_code.expired_at = medical_edit_code.created_at + \
                timezone.timedelta(hours=1)
            medical_edit_code.status = 'V'
            medical_edit_code.save()
        else:
            import random
            import string
            code = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))

            validated_data = {
                'patient': patient,
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
        print(request.data)
        if not medical_edit_code:
            return Response({'detail': 'Invalid medical edit code.'}, status=status.HTTP_400_BAD_REQUEST)

        if medical_edit_code.status == 'E' or dt.now().date() > medical_edit_code.expired_at.date():
            return Response({'detail': 'Medical edit code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the medical edit code from the request body
        medical_edit_code_value = request.data.get('code')
        if not medical_edit_code_value:
            return Response({'detail': 'Please enter a valid medical edit code.'}, status=status.HTTP_400_BAD_REQUEST)

        if medical_edit_code_value != medical_edit_code.code:
            return Response({'detail': 'Invalid medical edit code.'}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = {
            'patient': patient,
            'doctor': doctor,
        }

        base_url = request.scheme + '://' + request.get_host()
        return redirect(f'{base_url}/medical-entry/doctor/patient/list/{patient_id}/')
