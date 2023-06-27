from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'phone', 'gender',
                  'national_id', 'date_of_birth', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # Validating Password and Confirm Password while Registration

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
            # Custom password validation
        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."})

        if password.isnumeric():
            raise serializers.ValidationError(
                {"password": "Password cannot contain only numeric characters."})

        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
