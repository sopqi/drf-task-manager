from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import TasksViewSet, UserMeView

router = DefaultRouter()
router.register(r'tasks', TasksViewSet)
urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('me/', UserMeView.as_view()),
    path('', include(router.urls))
]