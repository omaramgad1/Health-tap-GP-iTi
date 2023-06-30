from rest_framework import serializers
from Patient.models import Patient
from MedicalCode.models import MedicalEditCode
import datetime
import pytz


class MedicalEditCodeSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    class Meta:
        model = MedicalEditCode
        fields = ['id', 'patient', 'code', 'created_at', 'expired_at', 'status']
        read_only_fields = ['id', 'created_at', 'expired_at', 'status']

    def create(self, validated_data):
        import random
        import string
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        validated_data['code'] = code
        validated_data['status'] = 'V'
        
        medical_edit_code = MedicalEditCode.objects.create(**validated_data)

        return medical_edit_code

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_at = datetime.datetime.strptime(representation["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Africa/Cairo")).strftime('%Y-%m-%d %H:%M:%S')
        expired_at = datetime.datetime.strptime(representation["expired_at"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Africa/Cairo")).strftime('%Y-%m-%d %H:%M:%S')
        representation["created_at"] = created_at
        representation["expired_at"] = expired_at

        if instance.is_valid() == False:
            representation['status'] = 'E'

        return representation