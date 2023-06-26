from django.urls import path
from User.api.views import PatientListCreateView, DoctorListCreateView , RegisterationAsPatient , RegisterationAsDoctor
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('list/patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('list/doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('patientregister/', RegisterationAsPatient.as_view(), name='register'),
    path('doctorregister/', RegisterationAsDoctor.as_view(), name='register'),

]