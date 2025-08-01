from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Profile,PendingUser


@admin.register(get_user_model())
class CustomUser(UserAdmin):
    ordering = ["date_joined"]
    list_display = [
        "email",
        "is_staff",
        "is_active",
    ]

    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(PendingUser)
class PendingUserAdmin(admin.ModelAdmin):
    pass
