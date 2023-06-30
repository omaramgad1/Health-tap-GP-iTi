from django.urls import path
from MedicalCode.api.views import MedicalEditCodeListCreateView , MedicalEditCodeRetrieveUpdateDeleteView

urlpatterns = [
    path('',MedicalEditCodeListCreateView.as_view(), name='medical_edit_code_list_create'),
    path('<int:pk>/', MedicalEditCodeRetrieveUpdateDeleteView.as_view(), name='medical_edit_code_retrieve_update_delete'),
]