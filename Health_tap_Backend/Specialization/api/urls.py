from django.urls import path
from Specialization.api.views import SpecializationListCreateView

urlpatterns = [
    path('', SpecializationListCreateView.as_view(),
         name='specialization-list-create'),
]
