from rest_framework import serializers

from accounts.utlis import phone_regex
from django.contrib.auth import get_user_model

User = get_user_model()


class SendOTPSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)
    phone = serializers.CharField(
        validators=[
            phone_regex,
        ]
    )

    class Meta:
        model = User
        fields = [
            "email",
            "phone",
            "password",
            "password1",
        ]


class SendLoginOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(
        validators=[
            phone_regex,
        ],
    )


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(
        validators=[
            phone_regex,
        ],
    )
    code = serializers.CharField()
