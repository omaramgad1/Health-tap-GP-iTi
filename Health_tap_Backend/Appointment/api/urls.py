from django.urls import path
from .views import *

urlpatterns = [

    path('doctor/add/', add_appointment, name='add_appointment'),

    path('doctor/list-all/', list_doctor_appointments,
         name='list_doctor_appointments'),

    path('doctor/list-history/', list_doctor_history_appointments,
         name='list_doctor_history_appointments'),

    path('doctor/list/available/', list_available_appointments,
         name='list_available_appointments'),

    path('doctor/list/reserved/', list_reserved_appointments,
         name='list_reserved_appointments'),

    path('doctor/list/today/available/', get_available_appointments,
         name='get_available_appointments'),

    path('doctor/list/today/reserved/', get_reserved_appointments,
         name='get_reserved_appointments'),

    path('doctor/list/count/status/', count_available_reserved_appointments,
         name='count_available_reserved_appointments'),

    path('doctor/edit/<int:appointment_id>/',
         edit_appointment, name='edit_appointment'),

    path('doctor/delete/<int:appointment_id>/',
         delete_appointment, name='delete_appointment'),

    path('doctor/list/date/<slug:date>/',
         list_doctor_appointments_by_date, name='list_doctor_appointments_by_date'),

    ###################### Patient #####################
    path('patient/doctor/<int:doctor_id>/available/',
         get_available_appointments_patient, name='get_available_appointments_patient'),


    path('patient/list/date/<slug:date>/',
         list_doctor_appointments_by_date_pateint, name='list_doctor_appointments_by_date_pateint'),

]
