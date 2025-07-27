from django.db import transaction
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.serializers import ValidationError

from ...models import PhoneOTP
from accounts.models import PendingUser
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from ...utils import generate_otp, send_otp_sms

User = get_user_model()


def sended_code_is_expired(phone):
    existing_otp = PhoneOTP.objects.filter(phone=phone).first()
    if existing_otp and not existing_otp.is_expired():
        raise ValidationError({"message": "Code already sent. Please wait."})


class RequestOTPApiView(GenericAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp'
    serializer_class = SendOTPSerializer

    def post(self, request):
        serializer = SendOTPSerializer(
            data=request.data,
        )
        with transaction.atomic():
            if serializer.is_valid():
                phone = serializer.validated_data["phone"]
                if not PendingUser.objects.filter(phone=phone).exists():
                    return Response(
                        {
                            "error": " Number is Activated Or There is not any user with this number"
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
                sended_code_is_expired(phone)
                code = generate_otp()
                PhoneOTP.objects.update_or_create(phone=phone, defaults={"code": code})
                send_otp_sms(phone, code)
                return Response({"message": "Verification Code Sended"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPApiView(GenericAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp'
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                phone = serializer.validated_data["phone"]
                code = serializer.validated_data["code"]
                try:
                    otp = PhoneOTP.objects.get(phone=phone, code=code)
                    if otp.is_expired():
                        return Response(
                            {"error": "code is expired"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    pending = PendingUser.objects.get(phone=phone)
                    user = User.objects.create_user(
                        email=pending.email,
                        phone=pending.phone,
                        password=pending.password,
                        is_active=True
                    )
                    otp.delete()
                    pending.delete()
                    return Response(
                        {"message": "Code Accepted And Account Verified"},
                        status=status.HTTP_200_OK,
                    )
                except PhoneOTP.DoesNotExist:
                    return Response(
                        {"error": "Code is Not Correct"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginRequestOTPApiView(GenericAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp'
    serializer_class = SendOTPSerializer

    def post(self, request):
        with transaction.atomic():
            serializer = SendOTPSerializer(
                data=request.data,
            )
            if serializer.is_valid():
                phone = serializer.validated_data["phone"]
                if not User.objects.filter(phone=phone, is_active=True).exists():
                    return Response(
                        {"error": "User not found or inactive"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                sended_code_is_expired(phone)
                code = generate_otp()
                PhoneOTP.objects.update_or_create(phone=phone, defaults={"code": code})
                send_otp_sms(phone, code)
                return Response({"message": "Verification Code Sended"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginVerifyOTPApiView(GenericAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            code = serializer.validated_data["code"]
            try:
                otp = PhoneOTP.objects.get(phone=phone, code=code)
                if otp.is_expired():
                    return Response(
                        {"error": "code is expired"}, status=status.HTTP_400_BAD_REQUEST
                    )
                otp.delete()
                user = User.objects.get(phone=phone)
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            except PhoneOTP.DoesNotExist:
                return Response(
                    {"error": "Code is Not Correct"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
