from django.contrib import admin

# Register your models here.
from task_manager.models import Category, Task, SubTask

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)