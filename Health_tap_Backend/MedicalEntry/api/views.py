from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import MedicalEntry
from .serializers import MedicalEntrySerializer
from Patient.models import Patient
from rest_framework import status
from .permissions import *
from django.db import transaction


@api_view(['GET'])
@permission_classes([IsPatient])
def patient_medical_entry_list(request):
    # Get the currently authenticated user (assumed to be a Patient)
    patient = request.user.patient

    print(request.user.patient.is_patient)
    print(patient)
    # Get the MedicalEntry objects for this patient
    medical_entries = MedicalEntry.objects.filter(
        patient=patient).order_by('-created_at')
    # Serialize the MedicalEntry objects
    serializer = MedicalEntrySerializer(medical_entries, many=True)
    # Return the serialized data
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsDoctor])
def patient_medical_entry_list_doctor(request, patient_id):
    try:
        patient = patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get the MedicalEntry objects for this patient
    medical_entries = MedicalEntry.objects.filter(
        patient=patient).order_by('-created_at')
    # Serialize the MedicalEntry objects
    serializer = MedicalEntrySerializer(medical_entries, many=True)
    # Return the serialized data
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsDoctor])
def medical_entry_create(request, patient_id, code):
    try:
        # Get the patient object from the request data
        patient = patient.objects.get(id=patient_id)

        # Get the medical edit code from the request data
        medical_edit_code = MedicalEditCode.objects.get(
            patient=patient, code=code)

        # Check if the medical edit code is valid
        if not medical_edit_code.is_valid():
            return Response({'message': 'The medical edit code is expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new MedicalEntry object
        serializer = MedicalEntrySerializer(data=request.data)
        if serializer.is_valid():
            # Save the new MedicalEntry object
            with transaction.atomic():
                # Save the new MedicalEntry object
                medical_entry = serializer.save(
                    doctor=request.user.doctor, patient=patient)

                # Set the medical edit code status to 'expired'
                medical_edit_code.status = 'E'
                medical_edit_code.save()

            # Return the serialized data for the new object
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except (Patient.DoesNotExist, MedicalEditCode.DoesNotExist):
        # Return a 404 error if the patient or medical edit code object doesn't exist
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsDoctor, IsDoctor_Edit_Medical_Entry])
def medical_entry_update(request, medical_entry_id, patient_id, code):
    try:

        # Get the patient object from the request data
        patient = patient.objects.get(id=patient_id)

        # Get the medical edit code from the request data
        medical_edit_code = MedicalEditCode.objects.get(
            patient=patient, code=code)

        # Check if the medical edit code is valid
        if not medical_edit_code.is_valid():
            return Response({'message': 'The medical edit code is expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the MedicalEntry object to update
        medical_entry = MedicalEntry.objects.get(id=medical_entry_id)

        serializer = MedicalEntrySerializer(medical_entry, data=request.data)
        if serializer.is_valid():
            # Save the updated MedicalEntry object
            with transaction.atomic():
                updated_medical_entry = serializer.save()

                # Return the serialized data for the updated object
                return Response(serializer.data, status=status.HTTP_200_OK)

    except MedicalEntry.DoesNotExist:
        # Return a 404 error if the MedicalEntry object doesn't exist
        return Response(status=status.HTTP_404_NOT_FOUND)
