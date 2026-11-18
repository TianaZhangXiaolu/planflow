
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task

        fields = [
            "id",
            "title",
            "project",
            "category",
            "description",
            "created_at",
            "updated_at",
            "is_completed",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_project(self, value):
        request = self.context["request"]

        if value.user != request.user:
            raise serializers.ValidationError(
                "You do not own this project."
            )

        return value

    def validate(self, attrs):
        project = attrs.get(
            "project",
            self.instance.project if self.instance else None
        )

        category = attrs.get(
            "category",
            self.instance.category if self.instance else None
        )

        if category and category.project_id != project.id:
            raise serializers.ValidationError(
                "This category does not belong to the selected project."
            )

        return attrs
