from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, Comment


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Not allowed in a deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Not the owner of the category")

        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
