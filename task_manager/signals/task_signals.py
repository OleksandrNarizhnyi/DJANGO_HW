from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from task_manager.models import Task


@receiver(pre_save, sender=Task)
def change_status_by_task_signal(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Task.objects.get(pk=instance.pk)
        if instance.status == 'Done':
            print('|'*100)
            send_mail(
                subject='Задача закрыта',
                message=f"Задача '{old_instance.title}' была закрыта.",
                from_email='no-reply@taskmanager.com',
                recipient_list=['recipient@example.com'],
                fail_silently=False,
            )
            print('|' * 100)

        elif old_instance.status != instance.status:
            print('|' * 100)
            send_mail(
                subject='Статус задачи изменён',
                message=f"Статус задачи '{old_instance.title}' изменён со статуса '{old_instance.status}' на '{instance.status}'.",
                from_email='no-reply@taskmanager.com',
                recipient_list=['admin.mail@gmail.com'],
                fail_silently=False,
            )
            print('|' * 100)

