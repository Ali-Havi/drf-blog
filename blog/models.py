from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    categories = models.ManyToManyField(
        "Category",
        related_name="blog_category",
        blank=True,
    )
    title = models.CharField(max_length=50)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} : {self.title}"


class Category(models.Model):
    title = models.CharField(max_length=125)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    status = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True)
