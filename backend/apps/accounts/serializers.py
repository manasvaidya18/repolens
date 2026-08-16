import secrets
from .services import EmailService
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
        )

    def create(self, validated_data):  

        token = secrets.token_urlsafe(32)

        user = User.objects.create_user(
        email=validated_data["email"],
        username=validated_data["username"],
        password=validated_data["password"],
        )

        user.email_verification_token = token
        user.save()

        EmailService.send_verification_email(user)

        return user