from django.urls import path
from .views import *

urlpatterns = [
    path('patient/list/', patient_medical_entry_list,
         name='patient_medical_entries'),

]
