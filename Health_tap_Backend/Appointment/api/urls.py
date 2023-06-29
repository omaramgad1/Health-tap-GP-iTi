from django.urls import path
from .views import *

urlpatterns = [

    path('doctor/add/', add_appointment, name='add_appointment'),
    
    path('doctor/list-all/', list_doctor_appointments,name='list_doctor_appointments'),
    
    path('doctor/list/available/', list_available_appointments,name='list_available_appointments'),
    
    path('doctor/list/reserved/', list_reserved_appointments,name='list_reserved_appointments'),
    
    path('doctor/edit/<int:appointment_id>/',edit_appointment, name='edit_appointment'),
    
    path('doctor/delete/<int:appointment_id>/',delete_appointment, name='delete_appointment'),


]
