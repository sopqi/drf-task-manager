from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Task


@receiver([post_save, post_delete], sender=Task)
def clear_task_cache(sender, instance, **kwargs):
    cache.clear()
    print("кэш очищен")