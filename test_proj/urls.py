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
from django.contrib import admin
from django.urls import path

from first_app.views import django_greetings, user_greetings
from task_manager.views import task_create, task_list, task_detail, task_statistic


urlpatterns = [
    path('admin/', admin.site.urls),
    path('greetings/', django_greetings),
    path('greetings/<str:name>/', user_greetings),

    path('tasks/create/', task_create),
    path('tasks/', task_list),
    path('tasks/<int:task_id>/', task_detail),
    path('tasks/statistic/', task_statistic),
]
