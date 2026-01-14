from rest_framework import serializers
from .models import Task, Comment, User


class SerializerComments(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at']
        read_only_fields = ['created_at']

class SerializerTasks(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = SerializerComments(many=True, read_only=True)
    executor_worker = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), default=None)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'author','executor_worker', 'comments', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        worker_tasks = SerializerTasks(many=True, read_only=True)
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name', 'worker_tasks']
        read_only_fields = ['role']