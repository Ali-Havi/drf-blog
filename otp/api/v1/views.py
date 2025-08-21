from django.db import transaction
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.serializers import ValidationError

from .serializers import SendLoginOTPSerializer, SendOTPSerializer, VerifyOTPSerializer
from ...utils import (
    generate_otp,
    send_otp_sms,
    sended_code_is_expired,
    save_otp,
    verify_otp,
    delete_pending_user,
    get_pending_user,
    save_pending_user,
)

User = get_user_model()


class RequestOTPApiView(GenericAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "otp"
    serializer_class = SendOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            if User.objects.filter(phone=phone).exists():
                return Response({"error": "Number already registered"}, status=400)

            save_pending_user(phone, email, password)

            resp = sended_code_is_expired(phone)
            if resp:
                return resp

            code = generate_otp()
            save_otp(phone, code)
            send_otp_sms(phone, code)

            return Response({"message": "Verification Code Sended"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPApiView(GenericAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "otp"
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            phone = serializer.validated_data["phone"]
            code = serializer.validated_data["code"]

            if not verify_otp(phone, code):
                return Response(
                    {"error": "Invalid or expired code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            pending = get_pending_user(phone)
            if not pending:
                return Response({"error": "Pending data expired"}, status=400)

            user = User.objects.create_user(
                email=pending["email"],
                phone=pending["phone"],
                password=pending["password"],
                is_active=True,
            )
            delete_pending_user(phone)

            return Response(
                {"message": "Code Accepted And Account Verified"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginRequestOTPApiView(GenericAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "otp"
    serializer_class = SendLoginOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            if not User.objects.filter(phone=phone, is_active=True).exists():
                return Response(
                    {"error": "User not found or inactive"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            sended_code_is_expired(phone)
            otp = generate_otp()
            save_otp(phone, otp)
            send_otp_sms(phone, otp)
            return Response({"message": "Verification Code Sended"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginVerifyOTPApiView(GenericAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            code = serializer.validated_data["code"]

            if not User.objects.filter(phone=phone, is_active=True).exists():
                return Response(
                    {"error": "User not found or inactive"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if sended_code_is_expired(phone) or not verify_otp(phone, code):
                return Response(
                    {"error": "Invalid or expired code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.get(phone=phone)
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
