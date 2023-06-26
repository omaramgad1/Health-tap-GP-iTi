from rest_framework import generics
from Specialization.models import Specialization
from Specialization.api.serializers import SpecializationSerializer

class SpecializationListCreateView(generics.ListCreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer