from django.db import models
from django.utils import timezone
from task_manager.mangers.categories import SoftDeleteManager

STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]

# Задание 2: Реализация мягкого удаления категорий
# Шаги для выполнения:
# Добавьте два новых поля в вашу модель Category, если таких ещё не было.
# В модели Category добавьте поля is_deleted(Boolean, default False) и deleted_at(DateTime, null=true)
# Переопределите метод удаления, чтобы он обновлял новые поля к соответствующим значениям: is_deleted=True и дата и время на момент “удаления” записи
# Переопределите менеджера модели Category
# В менеджере модели переопределите метод get_queryset(), чтобы он по умолчанию выдавал только те записи, которые не “удалены” из базы.

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()

        self.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ('name',)




class Task(models.Model):

    title = models.CharField(max_length=50, unique_for_date='deadline')
    description = models.CharField(max_length=300)
    categories =  models.ManyToManyField(Category)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        unique_together = ('title',)



class SubTask(models.Model):

    title = models.CharField(max_length=50, unique_for_date='deadline')
    description = models.CharField(max_length=300)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        unique_together = ('title',)

