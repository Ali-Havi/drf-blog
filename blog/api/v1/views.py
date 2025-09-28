from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from .permission import (
    IsAdminUserOrReadOnly,
    IsBlogOwnerOrReadOnly,
    IsCommentOwnerOrReadOnly,
    IsAuthenticatedOrReadOnly,
)
from .serializers import (
    BlogCreateAndUpdateSerializer,
    BlogSerializer,
    CategorySerializer,
    UserBlogSerializer,
    CommentSerializer,
)
from ...models import Blog, Category, Comment


class BlogViewSet(ModelViewSet):
    http_method_names = ["get", "head", "option", "post", "put", "delete"]
    serializer_class = BlogSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['categories','author']
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        return (
            Blog.objects.filter(status=True)
            .select_related("author")
            .prefetch_related("categories")
        )

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "detail": "Your post was successfully submitted and will be displayed after admin approval."
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "detail": "Your post was successfully updated and will be displayed after admin approval."
            },
            status=status.HTTP_200_OK,
        )


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
        qs = Comment.objects.select_related("author").filter(
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "detail": "Your Comment Successfully Posted and will be displayed after admin approval",
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "detail": "Your comment was successfully updated and will be displayed after admin approval."
            },
            status=status.HTTP_200_OK,
        )
