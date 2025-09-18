from django.urls import path, include

app_name = "otp"

urlpatterns = [
    path("api/v1/", include("otp.api.v1.urls")),
]
