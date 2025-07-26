import random

# from kavenegar import KavenegarAPI
# from django.conf import settings


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_sms(phone, code):
    # api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    params = {"receptor": phone, "message": f"Your Verification Code : {code}"}
    print(params)
    # api.sms_send(params)
