from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from Review.models import Review
from Appointment.models import Appointment
from Patient.models import Patient
from Doctor.models import Doctor
from .serializers import ReviewSerializer, PatientSerializer, DoctorSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from Review.pagination import ReviewPagination

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_reviews(request, doctor_id):
    pagination_class = ReviewPagination
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    reviews = Review.objects.filter(doctor=doctor)
    serializer = ReviewSerializer(reviews , many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, doctor_id):
    patient = request.user.patient  # Assuming the authenticated user is a patient
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(patient=patient, doctor=doctor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

