from django.urls import include, path


urlpatterns = [
    path("blog/api/v1/", include("blog.api.v1.urls")),
]
