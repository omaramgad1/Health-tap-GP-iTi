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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        patient_id = validated_data.get('patient').id

        if patient_id != request.user.patient.id:
            return Response({'detail': 'Patient ID in request data does not match authenticated patient ID.'}, status=status.HTTP_400_BAD_REQUEST)

        medical_edit_code = MedicalEditCode.objects.filter(patient=request.user.patient, status='V').first()
        if medical_edit_code:
            medical_edit_code.created_at = timezone.now()
            medical_edit_code.expired_at = medical_edit_code.created_at + timezone.timedelta(hours=1)
            medical_edit_code.status = 'V' 
            medical_edit_code.save()
        else:
            code = validated_data.get('code')
            if not code:
                import random
                import string
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                validated_data['code'] = code

            validated_data['created_at'] = timezone.now()
            validated_data['expired_at'] = validated_data['created_at'] + timezone.timedelta(hours=1)
            validated_data['status'] = 'V'

            medical_edit_code = MedicalEditCode.objects.create(**validated_data)

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


class PatientMedicalEntryListDoctorView(generics.ListAPIView):
    serializer_class = MedicalEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor = self.request.user.doctor
        if not doctor.is_doctor:
            return MedicalEntry.objects.none()

        patient_id = self.kwargs['patient_id']
        patient = get_object_or_404(Patient, id=patient_id)
        return MedicalEntry.objects.filter(patient=patient)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        patient_id = self.kwargs['patient_id']
        serializer = self.get_serializer(queryset, many=True)
        return redirect(f'http://localhost:8000/medical-entry/doctor/patient/list/{patient_id}/')

