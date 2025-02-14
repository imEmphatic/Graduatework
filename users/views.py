import time

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, AuthCode
from users.permissions import IsOwner, IsUserStaff
from users.serializers import (
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserStaffSerializer,
    UserVerifySerializer,
)
from users.services import generate_auth_code, generate_invite_code


class UserAuthAPIView(APIView):
    """Представление для авторизации пользователя"""

    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        user, created = User.objects.get_or_create(phone=phone)

        auth_code = generate_auth_code()

        AuthCode.objects.create(user=user, code=auth_code)

        print(f"Код для {phone}: {auth_code}")

        if created:
            user.invite_code = generate_invite_code()
            user.set_unusable_password()
            user.save()

        time.sleep(2)

        return Response({}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserVerifySerializer)
    def put(self, request, *args, **kwargs):
        """Метод для отправки на сервер полученного кода авторизации"""
        serializer = UserVerifySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data.get("phone")
        code = serializer.validated_data.get("auth_code")

        try:
            user = User.objects.get(phone=phone)
            auth_code = AuthCode.objects.get(user=user, code=code)
        except (User.DoesNotExist, AuthCode.DoesNotExist):
            return Response(
                {"message": "Доступ запрещен. Неверный код или номер телефона."},
                status=status.HTTP_403_FORBIDDEN,
            )

        auth_code.delete()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            {
                "message": "Доступ разрешен.",
                "access_token": access_token,
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK,
        )
