from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Task, Comment,User
from django.db.models import Count, Q



@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id','role', 'username', 'email')
    list_display_links = ('id', 'username')
    search_fields = ('author__username',)
    list_per_page = 20

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    #все колонки
    list_display = ('id', 'title', 'status','priority', 'author','executor_worker', 'created_at', 'comment_count' )
    #ссылки для перехода в редактирование
    list_display_links = ('id', 'title')
    # фильтры
    list_filter = ('status', 'created_at', 'author')
    #поиск
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    # пагинация
    list_per_page = 20

    #подсчет комметариев
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('author').annotate(comments_count = Count('comments'))
        return qs

    def comment_count(self, obj):
        return obj.comments_count

    comment_count.short_description = 'Кол-во комментариев'
    comment_count.admin_order_field = 'comments_count'

    def changelist_view(self, request, extra_context=None):
        stats = Task.objects.aggregate(total = Count('id'),
                                       todo = Count('id', filter= Q(status = 'todo')),
                                       in_progress = Count('id', filter=Q(status = 'proces')),
                                       done = Count('id', filter = Q(status = 'done')),
                                       )

        msg = (
            f"📊 СТАТИСТИКА: "
            f"Всего задач: {stats['total']} | "
            f"К выполнению: {stats['todo']} | "
            f"В процессе: {stats['in_progress']} | "
            f"Готово: {stats['done']}"
        )
        #зеленая плашка
        self.message_user(request, msg, level = 'INFO')
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('id', 'short_text', 'task', 'author', 'created_at')
    list_filter = ('created_at', 'author')

    # сокращение комента
    def short_text(self, obj):
        if len(obj.text) > 30:
            return obj.text[:27] + '...'
        return obj.text

    # Название колонки
    short_text.short_description = 'Текст'