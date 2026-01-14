from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from api.views import TasksViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls'))
]
