from django.urls import include, path

app_name = "blog"

urlpatterns = [
    path("blog/api/v1/", include("blog.api.v1.urls")),
]
