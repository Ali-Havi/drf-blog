import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import override_settings


@pytest.fixture(autouse=True)
def disable_throttling():
    with override_settings(
        REST_FRAMEWORK={
            "DEFAULT_THROTTLE_CLASSES": [],
            "DEFAULT_THROTTLE_RATES": {"login": "1000/day"},
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
        is_verified=True,
    )
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestAccountsApi:
    def test_registration_work_with_correct_data(self, api_client, disable_throttling):
        url = reverse("accounts:api-v1:users:registrations")
        data = {
            "email": "test@email.com",
            "phone": "+989011234567",
            "password": "test_password",
            "password1": "test_password",
        }

        response = api_client.post(url, data)

        assert response.status_code == 201

    def test_registration_fail_with_not_correct_data(
        self, api_client, disable_throttling
    ):
        url = reverse("accounts:api-v1:users:registrations")
        data = {
            "email": "test@email.com",
            "phone": "+989011234567",
            "password": "test_password",
        }

        response = api_client.post(url, data)

        assert response.status_code == 400

    def test_jwt_create_successfully_work(
        self, api_client, common_user, disable_throttling
    ):
        create_url = reverse("accounts:api-v1:users:jwt-create")
        create_data = {"email": "test@test.com", "password": "test_password"}
        create_response = api_client.post(create_url, create_data)

        assert create_response.status_code == 200
        assert "access" in create_response.data
        assert "refresh" in create_response.data

    def test_jwt_refresh_successfully_work(
        self, api_client, common_user, disable_throttling
    ):
        create_url = reverse("accounts:api-v1:users:jwt-create")
        create_data = {"email": "test@test.com", "password": "test_password"}
        create_response = api_client.post(create_url, create_data)

        assert create_response.status_code == 200
        assert "access" in create_response.data
        assert "refresh" in create_response.data

        refresh_url = reverse("accounts:api-v1:users:jwt-refresh")
        refresh_token = {"refresh": create_response.data["refresh"]}
        refresh_response = api_client.post(refresh_url, data=refresh_token)

        assert refresh_response.status_code == 200
        assert "access" in refresh_response.data

    def test_jwt_verify_successfully_work(
        self, api_client, common_user, disable_throttling
    ):
        create_url = reverse("accounts:api-v1:users:jwt-create")
        create_data = {"email": "test@test.com", "password": "test_password"}
        create_response = api_client.post(create_url, create_data)

        assert create_response.status_code == 200
        assert "access" in create_response.data
        assert "refresh" in create_response.data

        verify_url = reverse("accounts:api-v1:users:jwt-verify")
        access_token = {"token": create_response.data["access"]}
        verify_response = api_client.post(verify_url, access_token)

        assert verify_response.status_code == 200

    def test_jwt_login_and_profile_access(
        self, api_client, common_user, disable_throttling
    ):
        url = reverse("accounts:api-v1:users:jwt-create")
        data = {"email": "test@test.com", "password": "test_password"}
        response = api_client.post(url, data)

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

        access_token = response.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        profile_url = reverse("accounts:api-v1:profile")
        profile_response = api_client.get(profile_url)
        print(api_client._credentials)

        print(profile_response.data["detail"])

        print(profile_url)

        # assert profile_response.status_code == 200
        # assert profile_response.data["email"] == common_user.email
