from django.urls import path
from .views import *

urlpatterns = [
    path('register/', doctor_register, name='doctor_register'),
    path('list/', DoctorListCreateView.as_view(),
          name='doctor-list-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('city/<int:city_id>/', DoctorListByCityView.as_view()),
    path('district/<int:district_id>/', DoctorListByDistrictView.as_view()),
    path('specialization/<int:specialization_id>/', DoctorListBySpecializationView.as_view()),
    path('city/<int:city_id>/district/<int:district_id>/specialization/<int:specialization_id>/', DoctorListByCityDistrictSpecializationView.as_view()),
]
