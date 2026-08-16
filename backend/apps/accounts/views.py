from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from .services import EmailService

from .jwt_serializers import (
    CustomTokenObtainPairSerializer,
)

class CustomTokenObtainPairView(
    TokenObtainPairView
):
    serializer_class = (
        CustomTokenObtainPairSerializer
    )

class RegisterView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        EmailService.send_verification_email(
            user
        )

        return Response(
            {
                "message":
                "User created successfully.",
            },
            status=status.HTTP_201_CREATED,
        )

class VerifyEmailView(APIView):

    permission_classes = []

    def get(self, request, token):

        try:
            user = User.objects.get(
                email_verification_token=token
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error":
                    "Invalid verification token."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.email_verified = True
        user.email_verification_token = None

        user.save()

        return Response(
            {
                "message":
                "Email verified successfully."
            }
        )