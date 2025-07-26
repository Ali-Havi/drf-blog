from rest_framework import serializers

from accounts.utlis import phone_regex


class SendOTPSerializer(serializers.Serializer):
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
