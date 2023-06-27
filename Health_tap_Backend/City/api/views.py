from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import City
from .serializers import CitySerializer
from District.api.serializers import DistrictSerializer


@api_view(['GET'])
def get_cities(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_city(request, city_id):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CitySerializer(city)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_districts_by_city_id(request, city_id):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

    districts = city.districts.all()
    serializer = DistrictSerializer(districts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
