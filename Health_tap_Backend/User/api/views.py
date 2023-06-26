from django.shortcuts import render
from rest_framework import generics , status
from User.models import Patient,Doctor
from User.api.serializers import PatientSerializer,DoctorSerializer , UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    
class RegisterationAsPatient(generics.GenericAPIView):
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]
    
    def post(self,request:Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()
            response={
                "message":"user created Successfully",
                "data":serializer.data
            }
            return Response(data=response , status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class RegisterationAsDoctor(generics.GenericAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]
    
    def post(self,request:Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()
            response={
                "message":"user created Successfully",
                "data":serializer.data
            }
            return Response(data=response , status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors , status=status.HTTP_400_BAD_REQUEST)