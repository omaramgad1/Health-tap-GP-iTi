from .serializers import PatientRegistrationSerializer
from rest_framework import status ,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Patient.models import Patient
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.request import Request
# from rest_framework.views import APIView
from django.contrib.auth import authenticate
from ..tokens import create_jwt_pair_for_user
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def patient_register(request):
    if request.method == 'POST':
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                "message":"user created Successfully",
                "data":serializer.data
            }
            return Response(data=response , status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
        
class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientRegistrationSerializer
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

       
        patient = Patient.objects.filter(email=email).first()

        if patient is None:
            return Response(data={
                'message': 'Invalid Email or Password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not patient.is_active:
            return Response(data={
                'message': 'User account is disabled'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, patient.password):
            return Response(data={
                'message': 'Invalid Email or Password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        tokens = create_jwt_pair_for_user(patient)
        response = {
            'message': 'Login Successfully',
            'tokens': tokens,
            'is_patient': patient.is_patient
        }

        return Response(data=response, status=status.HTTP_200_OK)