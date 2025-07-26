from django.urls import path
from ..views import (
    UserProfileApiView,
)


urlpatterns = [
    path("", UserProfileApiView.as_view(), name="profile"),
]
