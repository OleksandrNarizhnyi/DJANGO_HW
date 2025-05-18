from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, filters
from django.db.models import Count, QuerySet
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from task_manager.permissions.owner_permissions import IsOwnerOrReadOnly
from task_manager.models import Task, SubTask, Category
from task_manager.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer,
)

class UserSubTasksListGenericView(ListAPIView):
    serializer_class = SubTaskSerializer

    def get_queryset(self):
        return SubTask.objects.filter(
            owner=self.request.user
        )


class SubTasklistCreateView(ListCreateAPIView):
    queryset: QuerySet[SubTask] = SubTask.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset: QuerySet[SubTask] = SubTask.objects.all()
    permission_classes = [
        IsOwnerOrReadOnly
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubTaskSerializer
        return SubTaskCreateSerializer


class UserTasksListGenericView(ListAPIView):
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        return Task.objects.filter(
            owner=self.request.user
        )

class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

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

    def perform_create(self, serializer):
        return serializer.seve(owner=self.request.user)

class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [
        IsOwnerOrReadOnly
    ]

    lookup_url_kwarg = 'task_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer
        return TaskCreateSerializer

# Задание 1: Реализация CRUD для категорий с использованием ModelViewSet
# Шаги для выполнения:
# Создайте CategoryViewSet, используя ModelViewSet для CRUD операций.
# Добавьте маршрут для CategoryViewSet.
# Добавьте кастомный метод count_tasks используя декоратор @action для подсчета количества задач, связанных с каждой категорией.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    @action(
        detail=False,
        methods=['get', ],
        url_path='statistic'
    )
    def get_tasks_count_by_category(self, request: Request) -> Response:
        categories_statistic = Category.objects.annotate(
            count_tasks=Count('task')
        )

        data = [
            {
                "id": c.id,
                "name": c.name,
                "count_tasks": c.count_tasks,
            }
            for c in categories_statistic
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )



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
