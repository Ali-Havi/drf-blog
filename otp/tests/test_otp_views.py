import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import override_settings

# from ..utils import


@pytest.fixture(autouse=True)
def disable_otp_and_login_throttling():
    with override_settings(
        REST_FRAMEWORK={
            "DEFAULT_THROTTLE_CLASSES": [
                "rest_framework.throttling.AnonRateThrottle",
                "rest_framework.throttling.UserRateThrottle",
                "rest_framework.throttling.ScopedRateThrottle",
            ],
            "DEFAULT_THROTTLE_RATES": {
                "anon": "10/minute",
                "user": "1000/day",
                "otp": "10000/minute",  
                "login": "10000/minute", 
            },
        }
    ):
        yield

@pytest.fixture
def common_user(db):
    user = get_user_model().objects.create_user(
        email="test@test.com",
        phone="+989123456789",
        password="test_password",
        is_active=True,
    )
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestOTPViews:
    def test_otp_register_work(self, api_client, disable_otp_and_login_throttling):
        send_otp_url = reverse("otp:api-v1:send_otp")

        phone = "+989123456789"
        send_otp_data = {
            "email": "test@test.com",
            "phone": phone,
            "password": "test_password",
            "password1": "test_password",
        }
        send_otp_response = api_client.post(send_otp_url, send_otp_data)

        assert send_otp_response.status_code == 200
        assert "message" in send_otp_response.data

        saved_code = cache.get(f"otp:{phone}")

        verify_otp_url = reverse("otp:api-v1:verify_otp")
        verify_otp_data = {"phone": phone, "code": saved_code}

        verify_otp_response = api_client.post(verify_otp_url, verify_otp_data)

        assert verify_otp_response.status_code == 200
        assert "message" in verify_otp_response.data

    def test_otp_login_work(self, api_client, common_user, disable_otp_and_login_throttling):
        login_send_otp_url = reverse("otp:api-v1:send_otp_for_login")
        phone = "+989123456789"
        login_send_otp_data = {
            "phone": phone,
        }

        login_send_otp_response = api_client.post(
            login_send_otp_url, login_send_otp_data
        )

        assert login_send_otp_response.status_code == 200
        assert "message" in login_send_otp_response.data

        saved_code = cache.get(f"otp:{phone}")
        login_verify_otp_url = reverse("otp:api-v1:verify_otp_for_login")

        login_verify_otp_data = {
            "phone": phone,
            "code": saved_code,
        }

        login_verify_otp_response = api_client.post(
            login_verify_otp_url, login_verify_otp_data
        )


        assert login_verify_otp_response.status_code == 200
        assert "access" in login_verify_otp_response.data
        assert "refresh" in login_verify_otp_response.data

        access = login_verify_otp_response.data['access']
        api_client.credentials(HTTP_AUTHORIZATION = f"Bearer {access}")
        
        profile_url = reverse('accounts:api-v1:profile')
        profile_response = api_client.get(profile_url)

        assert profile_response.status_code == 403
