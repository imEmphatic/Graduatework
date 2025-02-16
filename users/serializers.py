from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone",)


class UserVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    auth_code = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "email",
            "avatar",
            "phone",
            "city",
            "telegram_id",
            "invite_code",
            "referral_code",
            "referrals",
        )
        read_only_fields = ("invite_code", "referrals")

    def validate_referral_code(self, value):
        """Валидация реферального кода."""
        if not value:
            return value

        try:
            referral_user = User.objects.get(invite_code=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверный invite-код.")

        current_user = self.instance
        if current_user and current_user.referrals:
            raise serializers.ValidationError("Вы уже использовали invite-код.")

        return value

    def update(self, instance, validated_data):
        """Обновление профиля пользователя с учетом реферального кода."""
        referral_code = validated_data.pop("referral_code", None)
        if referral_code:
            referral_user = User.objects.get(invite_code=referral_code)
            instance.referrals = referral_user
            instance.referral_code = referral_code

        return super().update(instance, validated_data)


class UserStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone", "is_active", "is_staff", "is_superuser")
