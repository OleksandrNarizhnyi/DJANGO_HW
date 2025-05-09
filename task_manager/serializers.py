from rest_framework import serializers
from task_manager.models import Task, SubTask, Category
from django.utils import timezone


class TaskCreateSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']

    def validate_deadline(self, value: str):
        if value < timezone.now():
            raise serializers.ValidationError(
                {
                   "deadline": "Deadline cannot be in the past."
                }
            )
        return value


class TaskListSerializer(serializers.ModelSerializer):
     class Meta:
         model = Task
         fields = ['title', 'description', 'status', 'deadline']


class SubTaskSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()

    class Meta:
        model = SubTask
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):
    subtask_set = SubTaskSerializer(many=True)

    class Meta:
        model = Task
        fields = "__all__"
        # exclude = ['status', 'deadline'] - какие поля не будут отображаться


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def validate_name(self, value: str):
        if value:
            exists_name = Category.objects.filter(name=value).exists()
            if exists_name:
                raise serializers.ValidationError(
                    {
                        "name": "Category with this name already exists"
                    }
                )
        return value

    def create(self, validated_data: dict[str, str | int | float]) -> Category:
        return super().create(validated_data)

    def update(self, instance: Category, validated_data: dict[str, str | int | float]) -> Category:
        return super().update(instance, validated_data)



