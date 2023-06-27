
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import District


class DistrictSerializer(serializers.ModelSerializer):

    city = serializers.CharField(source='city.name_en', read_only=True)

    class Meta:
        model = District
        fields = ['id', 'name_ar', 'name_en', 'city']
