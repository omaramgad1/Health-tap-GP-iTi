from django.urls import path
from .views import *

urlpatterns = [
    path('doctor/list-all/', list_all_appointments, name='list_all_appointments'),
    path('doctor/list/available/', list_available_appointments,
         name='list_available_appointments'),
    path('doctor/edit/<int:appointment_id>/',
         edit_appointment, name='edit_appointment'),
    path('doctot/delete/<int:appointment_id>/delete/',
         delete_appointment, name='delete_appointment'),
    path('doctor/appointments/', list_doctor_appointments,
         name='list_doctor_appointments'),
    path('doctor/appointments/add/', add_appointment, name='add_appointment'),
]
