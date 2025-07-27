from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import transaction

from .permission import (
    IsAdminUserOrReadOnly,
    IsBlogOwnerOrReadOnly,
    IsCommentOwnerOrReadOnly,
)
from .serializers import (
    BlogCreateAndUpdateSerializer,
    BlogSerializer,
    CategorySerializer,
    UserBlogSerializer,
    CommentSerializer,
)
from ...models import Blog, Category, Comment


class CategoryViewSet(ModelViewSet):
    http_method_names = ["get", "head", "option", "post", "put", "delete"]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]


class BlogViewSet(ModelViewSet):
    http_method_names = ["get", "head", "option", "post", "put", "delete"]
    serializer_class = BlogSerializer
    queryset = (
        Blog.objects.prefetch_related("categories")
        .select_related("author")
        .filter(status=True)
    )
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_permissions(self):
        method = self.request.method
        if method in ["POST", "GET"]:
            return [
                IsAuthenticatedOrReadOnly(),
            ]

        if method in ["PUT", "DELETE"]:
            return [
                IsBlogOwnerOrReadOnly(),
            ]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT"]:
            return BlogCreateAndUpdateSerializer

        if self.request.user.is_staff:
            return BlogSerializer
        else:
            return UserBlogSerializer

    def get_serializer_context(self):
        return {
            "request": self.request,
        }


class CommentViewSet(ModelViewSet):
    http_method_names = [
        "get",
        "head",
        "option",
        "post",
        "put",
        "delete",
    ]
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        blog_pk = self.kwargs.get("blog_pk")
        qs = Comment.objects.select_related("blog__author", "author").filter(
            blog_id=blog_pk, status=True
        )
        return qs

    def get_permissions(self):
        method = self.request.method
        if method in ["POST", "GET"]:
            return [
                IsAuthenticatedOrReadOnly(),
            ]

        if method in ["PUT", "DELETE"]:
            return [
                IsCommentOwnerOrReadOnly(),
            ]

    def get_serializer_context(self):
        return {
            "request": self.request,
            "blog_id": self.kwargs.get("blog_pk"),
        }
