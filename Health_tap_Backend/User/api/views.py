# from django.shortcuts import render
# from rest_framework import generics , status
# from User.models import Patient,Doctor
# from User.api.serializers import PatientSerializer,DoctorSerializer , UserSerializer
# from rest_framework.permissions import AllowAny , IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.request import Request
# from rest_framework.views import APIView
# from django.contrib.auth import authenticate
# from ..tokens import create_jwt_pair_for_user
# from django.contrib.auth.hashers import check_password
# from User.models import User

# class PatientListCreateView(generics.ListCreateAPIView):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer


# class DoctorListCreateView(generics.ListCreateAPIView):
#     queryset = Doctor.objects.all()
#     serializer_class = DoctorSerializer

    
# class RegisterationAsPatient(generics.GenericAPIView):
#     serializer_class = PatientSerializer
#     permission_classes = [AllowAny]
    
#     def post(self,request:Request):
#         data = request.data
#         serializer = self.serializer_class(data=data)

#         if serializer.is_valid():
#             user = serializer.save()
#             response={
#                 "message":"user created Successfully",
#                 "data":serializer.data
#             }
#             return Response(data=response , status=status.HTTP_201_CREATED)
        
#         return Response(data=serializer.errors , status=status.HTTP_400_BAD_REQUEST)

# class RegisterationAsDoctor(generics.GenericAPIView):
#     serializer_class = DoctorSerializer
#     permission_classes = [AllowAny]
    
#     def post(self,request:Request):
#         data = request.data
#         serializer = self.serializer_class(data=data)

#         if serializer.is_valid():
#             user = serializer.save()
#             response={
#                 "message":"user created Successfully",
#                 "data":serializer.data
#             }
#             return Response(data=response , status=status.HTTP_201_CREATED)
        
#         return Response(data=serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request: Request):
#         email = request.data.get('email')
#         password = request.data.get('password')

       
#         user = User.objects.filter(email=email).first()

#         if user is None:
#             return Response(data={
#                 'message': 'Invalid Email or Password'
#             }, status=status.HTTP_401_UNAUTHORIZED)

#         if not user.is_active:
#             return Response(data={
#                 'message': 'User account is disabled'
#             }, status=status.HTTP_401_UNAUTHORIZED)

#         if not check_password(password, user.password):
#             return Response(data={
#                 'message': 'Invalid Email or Password'
#             }, status=status.HTTP_401_UNAUTHORIZED)

#         tokens = create_jwt_pair_for_user(user)
#         response = {
#             'message': 'Login Successfully',
#             'tokens': tokens
#         }

#         return Response(data=response, status=status.HTTP_200_OK)