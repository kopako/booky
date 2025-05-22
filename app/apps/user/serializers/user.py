import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..models.user import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = User
        fields = "__all__"
        # fields = ['username', 'password', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        return user

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        re_pattern = r'^[a-zA-Z]+$'

        if not re.match(re_pattern, first_name):
            raise serializers.ValidationError(
                {"first_name": "First name must contain only alphabet characters."}
            )
        if not re.match(re_pattern, last_name):
            raise serializers.ValidationError(
                {"last_name": "Last name must contain only alphabet characters."}
            )

        password = attrs.get('password')
        re_password = attrs.pop('re_password', None)

        if not password:
            raise serializers.ValidationError(
                {"password": "This field is Required."}
            )

        if not re_password:
            raise serializers.ValidationError(
                {"re_password": "This field is Required."}
            )

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError(
                {"re_password": "Password didn't match."}
            )

        return attrs
