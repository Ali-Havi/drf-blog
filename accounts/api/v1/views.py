from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from ...models import Profile

from .serializers import (
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    UserProfileSerializer,
)

User = get_user_model()
class UserRegistrationApiView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "email": serializer.validated_data["email"],
                    "phone": serializer.validated_data["phone"],
                }
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PasswordChangeApiView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        with transaction.atomic():
            self.user = self.get_object()
            serializer = self.get_serializer(
                data=request.data, context={"user": self.user}
            )
            if serializer.is_valid():
                self.user.set_password(serializer.validated_data.get("new_password"))
                self.user.save()
                data = {"detail": "Password Successfully Changed"}
                return Response(data=data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileApiView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related("user")

    def get_object(self):
        qs = self.get_queryset()
        obj = get_object_or_404(qs, user=self.request.user)
        return obj
