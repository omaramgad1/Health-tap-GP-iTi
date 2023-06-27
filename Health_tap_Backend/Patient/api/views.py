from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Patient
from .serializers import PatientSerializer, DoctorSerializer


@api_view(['POST'])
def register_patient(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(is_patient=True, is_active=False)
        patient = Patient.objects.create(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
