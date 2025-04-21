from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.db.models import Count, QuerySet
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from task_manager.models import Task, SubTask
from task_manager.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)


class SubTaskListCreateAPIView(APIView, PageNumberPagination):
    page_size = 5

    def get_queryset(self, request: Request):

        queryset: QuerySet[SubTask] = SubTask.objects.all()

        # FILTER PARAMS
        title = request.query_params.get('title')
        status_sub = request.query_params.get('status')

        # SORT PARAMS
        sort_by = 'created_at'
        sort_order = request.query_params.get('order', 'asc')

        if title:
            queryset = queryset.filter(
                task__title=title
            )

        if status:
            queryset = queryset.filter(
                status=status_sub
            )

        if sort_order == 'desc':
            sort_by = f"-{sort_by}"

            queryset = queryset.order_by(sort_by)

        return queryset

    def post(self, request: Request) -> Response:
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')

        if page_size and page_size.isdigit():
            return int(page_size)

        return self.page_size

    def get(self, request: Request) -> Response:
        subtasks = self.get_queryset(request=request)
        results = self.paginate_queryset(queryset=subtasks, request=request, view=self)
        serializer = SubTaskSerializer(results, many=True)

        return self.get_paginated_response(data=serializer.data)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request: Request, **kwargs) -> Response:
        try:
            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
        except SubTask.DoesNotExist:
            return Response(
                data={
                    "message": "Subtask not found",
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SubTaskSerializer(subtask)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, **kwargs) -> Response:
        try:
            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
        except SubTask.DoesNotExist:
            return Response(
                data={
                    "message": "Subtask not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskSerializer(instance=subtask, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request: Request, **kwargs) -> Response:
        try:
            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
        except SubTask.DoesNotExist:
            return Response(
                data={
                    "message": "Subtask not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        subtask.delete()

        return Response(
            data={
                "message": "Subtask was deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class TaskListAPIView(APIView):
    def get_queryset(self, request: Request):
        queryset: QuerySet[Task] = Task.objects.all()
        # FILTER PARAMS
        weekday = request.query_params.get('weekday')
        if weekday:
            try:
                weekday = int(weekday)
                queryset: QuerySet[Task] = Task.objects.filter(created_at__week_day=weekday)
                return queryset

            except ValueError:
                queryset = queryset.none()

        return queryset

    def get(self, request: Request) -> Response:
        try:
            queryset = self.get_queryset(request)
            serializer = TaskListSerializer(queryset, many=True)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except ValueError:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request: Request):
        serializer = TaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


# @api_view(['GET'])
# def task_list(request):
#     tasks = Task.objects.all()
#     serializer = TaskListSerializer(tasks, many=True)
#     return Response(serializer.data, status=200)

@api_view(['GET'])
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            {"message": "Task not found"},
        )

    serializer = TaskListSerializer(task)
    return Response(serializer.data, status=200)


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
