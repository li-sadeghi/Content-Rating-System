from rest_framework import serializers
from django.contrib import auth
from django.core import exceptions

User = auth.get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration.

    This serializer is used for creating new user accounts. It validates the
    required fields: `username`, `first_name`, `last_name`, and `password`.
    The password is hashed before being saved.

    Methods:
        create(validated_data): Creates a new user instance with the provided
            validated data, hashes the password, and saves the user.
    """

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):
        """Create a new user with the provided validated data."""
        try:
            user = User(
                username=validated_data["username"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
            )
            # Hash the password
            user.set_password(validated_data["password"])
            user.save()
            return user
        except KeyError as e:
            raise exceptions.ValidationError(f"Missing required field: {str(e)}")
