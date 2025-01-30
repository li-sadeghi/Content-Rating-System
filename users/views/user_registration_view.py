from rest_framework import generics
from rest_framework import permissions
from django.contrib import auth
from users import serializers

User = auth.get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """API view for user registration.

    This view allows users to register by creating a new account.
    It is an open API that does not require authentication and
    uses the `UserRegistrationSerializer` for validation and
    creation of the user.

    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer
