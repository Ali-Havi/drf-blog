from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from ...models import PhoneOTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from ...utils import generate_otp, send_otp_sms


class RequestOTPApiView(GenericAPIView):
    serializer_class = SendOTPSerializer

    def post(self, request):
        serializer = SendOTPSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            if (
                not get_user_model()
                .objects.get(phone=serializer.validated_data["phone"])
                .exists()
            ):
                phone = serializer.validated_data["phone"]
                code = generate_otp()
                PhoneOTP.objects.update_or_create(phone=phone, defaults={"code": code})
                send_otp_sms(phone, code)
                return Response({"message": "Verification Code Sended"})
            return Response(
                {"error": "This Number is Used"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPApiView(GenericAPIView):
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
                otp.verified = True
                otp.delete()
                user = get_user_model().objects.get(phone=phone)
                user.is_active = True
                user.save()
                return Response({"message": "Code Accepted"}, status=status.HTTP_200_OK)
            except PhoneOTP.DoesNotExist:
                return Response(
                    {"error": "Code is Not Correct"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
