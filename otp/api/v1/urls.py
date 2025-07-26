from django.urls import path
from .views import RequestOTPApiView, VerifyOTPApiView

urlpatterns = [
    path("send/", RequestOTPApiView.as_view(), name="send_otp"),
    path("verify/", VerifyOTPApiView.as_view(), name="verify_otp"),
]
