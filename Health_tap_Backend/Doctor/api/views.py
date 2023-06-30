from .serializers import DoctorRegistrationSerializer
from rest_framework import status ,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Doctor.models import Doctor
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.request import Request
# from rest_framework.views import APIView
from django.contrib.auth import authenticate
from ..tokens import create_jwt_pair_for_user
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def doctor_register(request):
    if request.method == 'POST':
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                "message":"user created Successfully",
                "data":serializer.data
            }
            return Response(data=response , status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
        
class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorRegistrationSerializer
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

       
        doctor = Doctor.objects.filter(email=email).first()

        if doctor is None:
            return Response(data={
                'message': 'Invalid Email or Password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not doctor.is_active:
            return Response(data={
                'message': 'User account is disabled'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, doctor.password):
            return Response(data={
                'message': 'Invalid Email or Password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        tokens = create_jwt_pair_for_user(doctor)
        response = {
            'message': 'Login Successfully',
            'tokens': tokens,
            'is_doctor': doctor.is_doctor,
            "doctor_id": doctor.id,
            "doctor_first_name" : doctor.first_name,
            "doctor_last_name" : doctor.last_name,
            "doctor_email":doctor.email,
            'doctor_date_of_birth':doctor.date_of_birth,
            "doctor_phone":doctor.phone,
            "doctor_national_id":doctor.national_id,
            "doctor_gender": doctor.gender,
            "doctor_specialization":doctor.specialization.name,
            "doctor_profLicenseNo":doctor.profLicenseNo,
            "doctor_city":doctor.city.name_ar,
            "doctor_district":doctor.district.name_ar,
            "doctor_address":doctor.address   
        }
    

        return Response(data=response, status=status.HTTP_200_OK)
    
    
class DoctorListByCityView(generics.ListAPIView):
    serializer_class = DoctorRegistrationSerializer

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return Doctor.objects.filter(city__id=city_id)
    
    
class DoctorListByDistrictView(generics.ListAPIView):
    serializer_class = DoctorRegistrationSerializer

    def get_queryset(self):
        district_id = self.kwargs['district_id']
        return Doctor.objects.filter(district__id=district_id)