import time

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
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
        """Метод для отправки на сервер номера телефона и получения кода авторизации"""
        serializer = UserRegistrationSerializer(data=request.data)
        message = "На указанный Вами номер телефона отправлено SMS с кодом доступа."

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data["phone"]
        user, created = User.objects.get_or_create(phone=phone)

        # Генерация кода
        user.auth_code = generate_auth_code()
        if created:
            user.invite_code = generate_invite_code()
        user.set_password(user.auth_code)
        user.save()

        time.sleep(2)
        return Response(
            {"message": message, "test_code": user.auth_code},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=UserVerifySerializer)
    def put(self, request, *args, **kwargs):
        """Метод для отправки на сервер полученного кода авторизации"""
        serializer = UserVerifySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data.get("phone")
        code = serializer.validated_data.get("auth_code")

        try:
            user = User.objects.get(phone=phone, auth_code=code)
        except User.DoesNotExist:
            return Response(
                {"message": "Доступ запрещен. Неверный код или номер телефона."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Выдача JWT-токенов
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


class UserProfileUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения и обновления профиля пользователя"""

    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsUserStaff]

    def update(self, request, *args, **kwargs):
        """Метод для обновления профиля пользователя"""
        data = request.data
        if "referral_code" not in data:
            return super().update(request, *args, **kwargs)

        try:
            referral_user = User.objects.get(invite_code=data["referral_code"])
            current_user = request.user

            if current_user.referrals:
                return Response(
                    {"message": "Вы уже использовали invite-код."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            current_user.referrals = referral_user  # Добавить реферала
            current_user.referral_code = data["referral_code"]
            current_user.save()
            return super().update(request, *args, **kwargs)

        except User.DoesNotExist:
            return Response(
                {"message": "Неверный invite-код."},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserListAPIView(generics.ListAPIView):
    """Представление для отображения списка пользователей для модератора"""

    serializer_class = UserStaffSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserStaff]
