"""
URL configuration for test_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from itertools import permutations

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from first_app.views import django_greetings, user_greetings
from task_manager.views import (
    TaskDetailUpdateDeleteView,
    task_statistic,
    SubTasklistCreateView,
    SubTaskDetailUpdateDeleteView,
    TaskListCreateView,
    CategoryViewSet,
    UserTasksListGenericView,
    UserSubTasksListGenericView,
    LogInAPIView,
    LogOutAPIView,
    RegisterUserAPIView,
)


schema_view = get_schema_view(
    openapi.Info(
        title='Tasks API',
        default_version='v1',
        description='Tasks API with permissions',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(name='Alex Narizhnyi', email='test.email@gmail.com'),
        license=openapi.License(name='OUR LICENSE', url='https://example.com')
    ),
    public=False,
    permission_classes=[permissions.IsAdminUser],
)

router = DefaultRouter()

router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('greetings/', django_greetings),
    path('greetings/<str:name>/', user_greetings),

    path('tasks/', TaskListCreateView.as_view()),
    path('tasks-me/', UserTasksListGenericView.as_view()),
    path('tasks/<int:task_id>/', TaskDetailUpdateDeleteView.as_view()),
    path('tasks/statistic/', task_statistic),

    path('subtasks/', SubTasklistCreateView.as_view()),
    path('subtasks-me/', UserTasksListGenericView.as_view()),
    path('subtasks/<int:pk>', UserSubTasksListGenericView.as_view()),

    path('', include(router.urls)),

    path('login/', LogInAPIView.as_view()),
    path('logout/', LogOutAPIView.as_view()),
    path('register/', RegisterUserAPIView.as_view()),

    path('auth-login/', TokenObtainPairView.as_view()),
    path('auth-refresh-token/', TokenRefreshView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]
