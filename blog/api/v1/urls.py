from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()

router.register(r"category", views.CategoryViewSet, basename="category")

router.register(r"", views.BlogViewSet, basename="blog")
nested_blog_router = NestedDefaultRouter(router, r"", lookup="blog")
nested_blog_router.register(r"comment", views.CommentViewSet, basename="comment")


urlpatterns = router.urls + nested_blog_router.urls
