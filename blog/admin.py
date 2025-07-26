from django.contrib import admin

from .actions import StatusActionsAdminModel
from .models import Blog, Category, Comment


@admin.register(Blog)
class BlogAdmin(StatusActionsAdminModel):
    list_display = ["id", "author", "title", "date_created", "status"]
    filter_horizontal = ["categories"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("author")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
    ]


@admin.register(Comment)
class CommentAdmin(StatusActionsAdminModel):
    list_display = [
        "id",
        "author_username",
        "blog_title",
        "comment",
        "status",
        "date_create",
    ]
    list_select_related = ["author", "blog"]

    def blog_title(self, obj):
        return f"{obj.blog.id} : {obj.blog.title}"

    def author_username(self, obj):
        return obj.author.email
