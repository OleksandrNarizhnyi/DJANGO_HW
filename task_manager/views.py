
from rest_framework import status, filters
from django.db.models import Count, QuerySet
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend

from task_manager.models import Task, SubTask
from task_manager.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)

# Задание 2: Замена представлений для подзадач (SubTasks) на Generic Views
# Шаги для выполнения:
# Замените классы представлений для подзадач на Generic Views:
# Используйте ListCreateAPIView для создания и получения списка подзадач.
# Используйте RetrieveUpdateDestroyAPIView для получения, обновления и удаления подзадач.
# Реализуйте фильтрацию, поиск и сортировку:
# Реализуйте фильтрацию по полям status и deadline.
# Реализуйте поиск по полям title и description.
# Добавьте сортировку по полю created_at.
class SubTasklistCreateView(ListCreateAPIView):
    queryset: QuerySet[SubTask] = SubTask.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubTaskSerializer
        return SubTaskCreateSerializer


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset: QuerySet[SubTask] = SubTask.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubTaskSerializer
        return SubTaskCreateSerializer

# Задание 1: Замена представлений для задач (Tasks) на Generic Views
# Шаги для выполнения:
# Замените классы представлений для задач на Generic Views:
# Используйте ListCreateAPIView для создания и получения списка задач.
# Используйте RetrieveUpdateDestroyAPIView для получения, обновления и удаления задач.
# Реализуйте фильтрацию, поиск и сортировку:
# Реализуйте фильтрацию по полям status и deadline.
# Реализуйте поиск по полям title и description.
# Добавьте сортировку по полю created_at.

class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskListSerializer
        return TaskCreateSerializer


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()

    lookup_url_kwarg = 'task_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer
        return TaskCreateSerializer



def task_statistic(request):
    count_task = Task.objects.aggregate(total_tasks=Count('id'))
    count_task_by_status = Task.objects.values('status').annotate(task_count=Count('id'))
    status_counts = {item['status']: item['task_count'] for item in count_task_by_status}
    pending_tasks = Task.objects.filter(status='pending').count()
    response_data = {
        'count_task': count_task['total_tasks'],
        'pending_tasks': pending_tasks,
        'count_task_by_status': status_counts
    }
    return JsonResponse(response_data)
