import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_proj.settings')
django.setup()

from task_manager.models import *
from datetime import datetime, timedelta
from django.db.models import Q, F

Task.objects.create(
    title='Prepare presentation',
    description='Prepare materials and slides for the presentation',
    status='New',
    deadline=datetime.today() + timedelta(days=3),
)


task = Task.objects.filter(
    task_id=4
)
subtasks = [
    SubTask(
        title='Gather information',
        description='Find necessary information for the presentation',
        status='New',
        task=task,
        deadline=datetime.today() + timedelta(days=2),),
    SubTask(
        title='Create slides',
        description='Create presentation slides',
        status='New',
        task=task,
        deadline=datetime.today() + timedelta(days=1),
),
]
SubTask.objects.bulk_create(subtasks)

task_new = Task.objects.filter(
    status="New"
)
print(task_new)

subtask_done = SubTask.objects.filter(
    Q(status="Done") & Q(deadline__lt=datetime.today())
)
print(subtask_done)

chang_task = Task.objects.get(title="Prepare presentation")
chang_task.status = "In progress"
chang_task.save()

SubTask.objects.filter(title="Gather information").update(deadline=F('deadline') - timedelta(days=2))

SubTask.objects.filter(title="Create slides").update(description="Create and format presentation slides")


deleted, _ = Task.objects.filter(title="Prepare presentation").delete()

print(f"Удалено {deleted} записей -> {_}")
