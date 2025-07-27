from django.contrib import admin

from .models import PhoneOTP


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    pass
