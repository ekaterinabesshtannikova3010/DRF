from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.contrib import admin
from .apps import MaterialsConfig
from .views import CourseViewSet, LessonListCreate, LessonDetail

app_name = MaterialsConfig.name

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreate, LessonDetail

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreate.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetail.as_view(), name='lesson-detail'),
]