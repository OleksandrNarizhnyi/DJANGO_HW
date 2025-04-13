from django.contrib import admin

# Register your models here.
from task_manager.models import Category, Task, SubTask
from django.db.models import QuerySet

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline')
    search_fields = ('title',)
    list_filter = ('status', 'deadline')

    actions = ['update_status_to_done']

    def update_status_to_done(self, request, objects: QuerySet) -> None:
        for obj in objects:
            obj.status = 'Done'

            obj.save()

    update_status_to_done.short_description = "Change status to Done"


class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]

    list_display = ('title', 'short_title', 'status', 'deadline')
    search_fields = ('title',)
    list_filter = ('status', 'deadline')

    def short_title(self, obj: Task) -> str:
        return f"{obj.title[:10]}..."


# admin.site.register(Category)
# admin.site.register(Task)
# admin.site.register(SubTask)


# Задание 1:
# Добавить настройку инлайн форм для админ класса задач. При создании задачи должна появиться возможность
# создавать сразу и подзадачу.
# Задание 2:
# Названия задач могут быть длинными и ухудшать читаемость в Админ панели, поэтому требуется выводить в списке
# задач укороченный вариант – первые 10 символов с добавлением «...», если название длиннее, при этом при
# выборе задачи для создания подзадачи должно отображаться полное название. Необходимо реализовать такую
# возможность.
# Задание 3:
# Реализовать свой action для Подзадач, который поможет выводить выбранные в Админ панели объекты в статус
# Done
