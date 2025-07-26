from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


from ..views import (
    UserRegistrationApiView,
    CustomTokenObtainPairView,
    PasswordChangeApiView,
)


urlpatterns = [
    # Register
    path("registration/", UserRegistrationApiView.as_view(), name="registrations"),
    # Change Password
    path("password/change/", PasswordChangeApiView.as_view(), name="change-password"),
    # Reset Password
    # JWT Token
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
