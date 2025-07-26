from django.db import models
from django.utils import timezone
from datetime import timedelta

from accounts.utlis import phone_regex


class PhoneOTP(models.Model):
    phone = models.CharField(
        validators=[phone_regex],
        max_length=14,
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def is_expired(self):
        elapsed = timezone.now() - self.created_at
        return elapsed > timedelta(minutes=2)