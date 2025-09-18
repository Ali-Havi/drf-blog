from rest_framework_nested.routers import (
    DefaultRouter,
    NestedDefaultRouter,
    NestedSimpleRouter,
)

from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register(r"category", views.CategoryViewSet, basename="category")
router.register(r"blogs", views.BlogViewSet, basename="blog")

nested_blog_router = NestedSimpleRouter(router, r"blogs", lookup="blog")
nested_blog_router.register(r"comment", views.CommentViewSet, basename="comment")


urlpatterns = router.urls + nested_blog_router.urls
