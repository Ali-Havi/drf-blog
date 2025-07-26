from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model

from ...models import Blog, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="category-detail")

    class Meta:
        model = Category
        fields = [
            "title",
            "url",
        ]


class BlogSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="blog-detail")
    author = serializers.StringRelatedField()
    categories = CategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Blog
        fields = [
            "author",
            "categories",
            "title",
            "text",
            "date_created",
            "status",
            "url",
        ]


class UserBlogSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="blog-detail")
    author = serializers.StringRelatedField()
    categories = CategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Blog
        fields = [
            "author",
            "categories",
            "title",
            "text",
            "url",
            "date_created",
        ]


class BlogCreateAndUpdateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
    )

    class Meta:
        model = Blog
        fields = [
            "title",
            "text",
            "categories",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            categories = validated_data.pop("categories", [])
            user = self.context["request"].user
            status = True if user.is_staff else False
            blog = Blog.objects.create(author=user, status=status, **validated_data)
            blog.categories.set(categories)
            return blog

    def update(self, instance, validated_data):
        with transaction.atomic():
            categories = validated_data.pop("categories", None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.status = False
            instance.save()
            if categories is not None:
                instance.categories.set(categories)
            return instance


class CommentBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = []


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    # blog = UserBlogSerializer()

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "comment",
            "date_create",
        ]
        read_only_fields = [
            "id",
            "author",
            "blog",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context["request"].user
            blog_id = self.context["blog_id"]
            status = True if user.is_staff else False
            return Comment.objects.create(
                author=user, blog_id=blog_id, status=status, **validated_data
            )

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.status = False
            instance.save()
            return instance
