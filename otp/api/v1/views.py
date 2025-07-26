from django.db import transaction
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


from ...models import PhoneOTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from ...utils import generate_otp, send_otp_sms

User = get_user_model()


class RequestOTPApiView(GenericAPIView):
    serializer_class = SendOTPSerializer

    def post(self, request):
        serializer = SendOTPSerializer(
            data=request.data,
        )
        with transaction.atomic():
            if serializer.is_valid():
                phone = serializer.validated_data["phone"]
                if not User.objects.filter(phone=phone, is_active=False).exists():
                    return Response(
                        {"error": " Number is Activated Or There is not any user with this number"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                code = generate_otp()
                PhoneOTP.objects.update_or_create(phone=phone, defaults={"code": code})
                send_otp_sms(phone, code)
                return Response({"message": "Verification Code Sended"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPApiView(GenericAPIView):
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
                    otp.verified = True
                    otp.delete()
                    user = User.objects.get(phone=phone)
                    user.is_active = True
                    user.save()
                    return Response(
                        {"message": "Code Accepted And Account Verified"}, status=status.HTTP_200_OK
                    )
                except PhoneOTP.DoesNotExist:
                    return Response(
                        {"error": "Code is Not Correct"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginRequestOTPApiView(GenericAPIView):
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
                code = generate_otp()
                PhoneOTP.objects.update_or_create(phone=phone, defaults={"code": code})
                send_otp_sms(phone, code)
                return Response({"message": "Verification Code Sended"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginVerifyOTPApiView(GenericAPIView):
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
