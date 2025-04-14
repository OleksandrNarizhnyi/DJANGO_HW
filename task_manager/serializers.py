from rest_framework import serializers
from task_manager.models import Task

class TaskCreateSerializer(serializers.ModelSerializer):
     class Meta:
         model = Task
         fields = ['title', 'description', 'status', 'deadline']


class TaskListSerializer(serializers.ModelSerializer):
     class Meta:
         model = Task
         fields = ['title', 'description', 'status', 'deadline']


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"