# from django.test import TestCase
# from django.contrib.auth import get_user_model

# from ..models import Blog,Category

# class TestBlogModel(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = get_user_model().objects.create_user(
#             email='test@test.com',
#             phone = '+989123456789',
#             password="test_password",
#         )
#         cls.category = Category.objects.create(title='test_category')

#     def test_create_a_blog_post(self):
#         post = Blog.objects.create(
#             author = self.user,
#             title = 'title_test',
#             text = 'test_text',
#             status = True
#         )
#         post.categories.add(self.category)
#         self.assertTrue(post.title, 'title_test')
