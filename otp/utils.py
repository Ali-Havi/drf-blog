import json
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
import random

# from kavenegar import KavenegarAPI
# from django.conf import settings


OTP_TTL = 120
PENDING_TTL = 600


def generate_otp():
    return str(random.randint(100000, 999999))


def save_pending_user(phone, email, password):
    data = {"email": email, "phone": phone, "password": password}
    cache.set(f"pending:{phone}", json.dumps(data), timeout=PENDING_TTL)


def get_pending_user(phone):
    raw_data = cache.get(f"pending:{phone}")
    if raw_data:
        return json.loads(raw_data)
    return None


def delete_pending_user(phone):
    cache.delete(f"pending:{phone}")


def code_is_sended(phone):
    if cache.get(f"otp:{phone}"):
        return Response(
            {"message": "You have already received a code. Please wait."},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )


def save_otp(phone, code):
    cache.set(f"otp:{phone}", code, timeout=OTP_TTL)


def verify_otp(phone, code):
    saved_code = cache.get(f"otp:{phone}")
    if saved_code and saved_code == code:
        cache.delete(f"otp:{phone}")
        return True
    return False


def send_otp_sms(phone, code):
    # api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    params = {
        "receptor": phone,
        "message": f"Your Verification Code : {code}",
    }
    print(params)
    # api.sms_send(params)
