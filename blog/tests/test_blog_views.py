import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from ..models import Blog, Comment


@pytest.fixture
def common_user(db):
    user = get_user_model().objects.create_user(
        email="test@test.com",
        phone="+989123456789",
        password="test_password",
        is_active=True,
    )
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestBlogAPi:

    def test_get_blog_list_response_200_status(self, api_client):
        url = reverse("blog:api-v1:blog-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_blog_response_401_status(self, api_client):
        url = reverse("blog:api-v1:blog-list")
        data = {
            "title": "test post title",
            "text": "test post text",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_blog_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("blog:api-v1:blog-list")
        data = {
            "title": "test post title",
            # We Dont POST "text" for testing
        }
        user = common_user
        login = api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_blog_crud_works(self, common_user, api_client):

        # Create Blog "POST"
        blog_list_url = reverse("blog:api-v1:blog-list")
        post_data = {
            "title": "test post title",
            "text": "test post text",
        }
        user = common_user
        login = api_client.force_authenticate(user=user)
        post_response = api_client.post(blog_list_url, post_data)

        assert post_response.status_code == 201

        # Read Blog "Get"
        blog_instance = Blog.objects.get(title="test post title")
        blog_instance.status = True
        blog_instance.save()

        blog_detail_url = reverse(
            "blog:api-v1:blog-detail",
            kwargs={
                "pk": blog_instance.pk,
            },
        )
        get_response = api_client.get(blog_detail_url)

        assert Blog.objects.filter(title="test post title").exists()
        assert get_response.status_code == 200

        # Update Blog "PUT"
        put_data = {
            "title": "test Update title",
            "text": "test Update text",
        }

        put_response = api_client.put(blog_detail_url, put_data)

        assert put_response.status_code == 200

        # Delete Blog "DELETE"
        blog_instance.status = True
        blog_instance.save()
        delete_response = api_client.delete(blog_detail_url)

        assert delete_response.status_code == 204

    def test_comment_crud_works(self, api_client, common_user):
        # Define a Blog Post

        user = common_user
        blog_instance = Blog.objects.create(
            author=user,
            title="Test Blog Title",
            text="Test Blog Text",
            status=True,
        )
        login = api_client.force_authenticate(user=user)

        # Read Comments List "GET"
        comment_list_url = reverse(
            "blog:api-v1:comment-list", kwargs={"blog_pk": blog_instance.pk}
        )

        comment_get_response = api_client.get(comment_list_url)

        assert comment_get_response.status_code == 200

        # Create Comment "POST"
        comment_list_url = reverse(
            "blog:api-v1:comment-list", kwargs={"blog_pk": blog_instance.pk}
        )
        comment_post_data = {"comment": "test Comment"}

        comment_post_response = api_client.post(comment_list_url, comment_post_data)

        assert comment_post_response.status_code == 201

        # Comment Detail "GET"
        comment_instance = Comment.objects.get(comment="test Comment")
        comment_instance.status = True
        comment_instance.save()

        comment_detail_url = reverse(
            "blog:api-v1:comment-detail",
            kwargs={"blog_pk": blog_instance.pk, "pk": comment_instance.pk},
        )

        comment_detail_response = api_client.get(comment_detail_url)

        assert comment_detail_response.status_code == 200

        # Update Comment "PUT"
        comment_put_data = {"comment": "test Update Comment"}
        comment_put_response = api_client.put(comment_detail_url, comment_put_data)

        assert comment_put_response.status_code == 200
