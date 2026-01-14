from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE = (
    ('user', 'Пользователь'),
    ('admin', 'Админ'),
    ('superadmin', 'Суперадмин'),
    )
    role = models.CharField(max_length=10, choices=ROLE, default='user')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Task(models.Model):
    STATUS = (
        ('todo', 'К выполнению'),
        ('proces', 'Выполняется'),
        ('done', 'Завершена'),
        ('canceled', 'Отменена' )
    )

    PRIORITY = (('low', 'Низкий'),
                ('medium', 'Средний'),
                ('high', 'Высокий'))

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description =  models.TextField(verbose_name='Описание', default='Описания нету')
    status = models.CharField(choices=STATUS, default='todo')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null =True, blank=True )
    executor_worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name='worker_tasks')
    priority = models.CharField(choices=PRIORITY, default='medium')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name = 'comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
