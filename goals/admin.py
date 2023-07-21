from django.contrib import admin

from goals.models import GoalCategory, Goal, Comment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal)
admin.site.register(Comment)
