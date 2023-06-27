from rest_framework import serializers
from Specialization.models import Specialization

<<<<<<< HEAD

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']
=======
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']
>>>>>>> aa1979b0426c63620f331414a9dd63dd206c0d3a
