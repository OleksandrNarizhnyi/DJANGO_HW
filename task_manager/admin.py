from django.contrib import admin

# Register your models here.
from task_manager.models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline')
    search_fields = ('title',)
    list_filter = ('status', 'deadline')


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline')
    search_fields = ('title',)
    list_filter = ('status', 'deadline')


# admin.site.register(Category)
# admin.site.register(Task)
# admin.site.register(SubTask)