from django.urls import path
from .views import *

urlpatterns = [
    path('patient/list/', patient_medical_entry_list,
         name='patient_medical_entries'),


    path('doctor/patient/list/<int:patient_id>/', patient_medical_entry_list_doctor,
         name='patient_medical_entry_list_doctor'),

    path('doctor/create/patient/<int:patient_id>/appointment/<int:appointment_id>/', medical_entry_create,
         name='medical_entry_create'),

    path('doctor/update/<int:medical_entry_id>/patient/<int:patient_id>/appointment/<int:appointment_id>/', medical_entry_update,
         name='medical_entry_update'),

    path('patient/<int:patient_id>/medical-entries/',
         PatientMedicalEntryList.as_view(), name='medical-entry-list')
]
