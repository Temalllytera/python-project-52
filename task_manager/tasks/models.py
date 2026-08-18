from django.contrib.auth.models import User
from django.db import models

from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Имя',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Статус',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name='Автор',
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        null=True,
        blank=True,
        verbose_name='Исполнитель',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name
