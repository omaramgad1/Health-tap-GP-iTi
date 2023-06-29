from django.urls import path
from .views import *

urlpatterns = [
    path('register/', patient_register, name='patient_register'),
    path('list/patient/', PatientListCreateView.as_view(),
          name='patient-list-create'),
    path('login/', LoginView.as_view(), name='login'),

]
