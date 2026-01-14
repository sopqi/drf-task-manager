

from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task, User
from .permissions import IsAuthorOrReadOnly, AdminOrReadOnly
from .serializers import SerializerTasks, SerializerComments, UserSerializer


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = SerializerTasks
    #настройка фильтрации
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # точная фильтрация
    filterset_fields = ['status', 'author']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'status']
    #сортировка по умолчанию
    ordering = ['-created_at']


    def get_permissions(self):
        if self.action == 'comments':
            return [permissions.IsAuthenticated(),]
        return  [permissions.IsAuthenticated(), AdminOrReadOnly(), IsAuthorOrReadOnly()]
    # 1. КЭШИРУЕМ СПИСОК ЗАДАЧ (list)
    @method_decorator(cache_page(60 * 5))  # 5 минут (60 сек * 5)
    @method_decorator(vary_on_headers("Authorization")) # Важно! Иначе Вася увидит кэш Пети
    def list(self, request, *args, **kwargs):
        # super().list(...) вызывает стандартный код получения списка
        return super().list(request, *args, **kwargs)

    # 2. КЭШИРУЕМ ДЕТАЛИ ЗАДАЧИ (retrieve - получение одной задачи)
    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)



    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

    # создания нового юрл для комментариев
    @action(detail=True, methods=['post'])
    def comments(self, request, pk = None):
        task = self.get_object()
        serializer = SerializerComments(data=request.data)

        if serializer.is_valid():
            serializer.save(author = request.user, task = task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user