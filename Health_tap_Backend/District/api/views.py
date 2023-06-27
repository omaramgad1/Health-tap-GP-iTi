
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import District
from .serializers import DistrictSerializer
from City.models import City


@api_view(['GET'])
def get_districts(request):
    districts = District.objects.all()
    serializer = DistrictSerializer(districts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
