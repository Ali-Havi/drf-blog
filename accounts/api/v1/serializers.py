from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import exceptions

from ...models import Profile
from ...utlis import phone_regex


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)
    phone = serializers.CharField(
        validators=[
            phone_regex,
        ]
    )

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "phone",
            "password",
            "password1",
        ]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "Passwords doesn't match"})
        try:
            validate_password(attrs.get("password"))

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return get_user_model().objects.create_user(**validated_data)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, required=True)
    new_password = serializers.CharField(max_length=255, required=True)
    new_password1 = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        if not self.context.get("user").check_password(attrs.get("old_password")):
            raise serializers.ValidationError({"password": "Password is not Correct"})

        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError(
                {"password": "New Passwords doesn't match"}
            )

        if attrs.get("old_password") == attrs.get("new_password"):
            raise serializers.ValidationError(
                {
                    "password": "New Password Cant be Same With Old Password",
                }
            )
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "email", "first_name", "last_name"]
