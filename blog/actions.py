from django.contrib import admin


@admin.action(description="Change Comments Status To True .")
def make_status_true(modeladmin, request, queryset):
    updated = queryset.update(status=True)
    modeladmin.message_user(request, f"{updated} Comments Status Changed To True")


@admin.action(description="Change Comments Status To False .")
def make_status_false(modeladmin, request, queryset):
    updated = queryset.update(status=False)
    modeladmin.message_user(request, f"{updated} Comments Status Changed To False")


class StatusActionsAdminModel(admin.ModelAdmin):
    actions = [make_status_true, make_status_false]
