from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r"^\+989\d{9}$",
)
