from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        """
        Create a new user instance with the validated data.
        """
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user Login.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user_instance = User.objects.filter(email=attrs["email"]).first()
        if not (user_instance and user_instance.check_password(attrs["password"])):
            raise serializers.ValidationError("Invalid credentials")
        self.instance = user_instance
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
