
from rest_framework import serializers
from Patient.models import Patient


class PatientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone', 'national_id', 'profileImgUrl',
                  'password', 'confirm_password', 'gender']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        del validated_data['confirm_password']
        patient = Patient.objects.create_patient(**validated_data)
        return patient

