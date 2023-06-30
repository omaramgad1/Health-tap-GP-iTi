from rest_framework import serializers
from Patient.models import Patient
from MedicalCode.models import MedicalEditCode


class MedicalEditCodeSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    class Meta:
        model = MedicalEditCode
        fields = ['id', 'patient', 'code', 'created_at', 'expired_at', 'status']
        read_only_fields = ['id', 'created_at', 'expired_at', 'status']

    def create(self, validated_data):
        # generate a random code
        import random
        import string
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        validated_data['code'] = code

        # create the medical edit code object
        medical_edit_code = MedicalEditCode.objects.create(**validated_data)

        return medical_edit_code