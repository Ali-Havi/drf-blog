from django.urls import path
from .views import RequestOTPApiView, VerifyOTPApiView , LoginRequestOTPApiView, LoginVerifyOTPApiView

urlpatterns = [
    path("send/", RequestOTPApiView.as_view(), name="send_otp"),
    path("verify/", VerifyOTPApiView.as_view(), name="verify_otp"),
    path("login/send/",LoginRequestOTPApiView.as_view(), name="send_otp_for_login"),
    path("login/verify/",LoginVerifyOTPApiView.as_view(), name="verify_otp_for_login"),
]
