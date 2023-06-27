from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import City
from District.api.serializers import DistrictSerializer


class CitySerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(
        many=True, read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name_ar', 'name_en', 'districts']
