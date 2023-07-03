from django.urls import path
from Specialization.api.views import SpecializationListCreateView , SpecializationNameView

urlpatterns = [
    path('', SpecializationListCreateView.as_view(),
         name='specialization-list-create'),
    
    path('<int:pk>/', SpecializationNameView.as_view(), name='specialization-name'),
]
