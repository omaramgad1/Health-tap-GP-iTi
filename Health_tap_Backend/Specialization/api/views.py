from rest_framework import generics
from Specialization.models import Specialization
from Specialization.api.serializers import SpecializationSerializer
from rest_framework.response import Response
from rest_framework import status

class SpecializationListCreateView(generics.ListCreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    
    
class SpecializationNameView(generics.RetrieveAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        specialization_id = self.kwargs.get('pk')
        if specialization_id:
            queryset = queryset.filter(id=specialization_id)
        return queryset 