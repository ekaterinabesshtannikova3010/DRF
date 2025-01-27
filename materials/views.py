from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .tasks import send_course_update_email
from users.models import Payment
from .models import Course, Lesson
from .paginators import CoursesPagination, LessonsPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CourseSerializer
    permission_classes = []
    pagination_class = CoursesPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_courses = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_courses, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(user=user)
        return Course.objects.none()

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Операция создания недоступна."},
                        status=403)

    def perform_update(self, serializer):
        # Логика для обновления урока
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Операция удаления недоступна."},
                        status=403)

    def update_course(request, course_id):
        course = get_object_or_404(Course, id=course_id)
        # Логика обновления курса
        course.title = request.POST.get('title', course.title)
        course.description = request.POST.get('description', course.description)
        course.save()

        # Вызов асинхронной задачи отправки письма
        send_course_update_email.delay(course.id)

        return JsonResponse({'status': 'success', 'message': 'Курс обновлён'})


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LessonsPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Lesson.objects.filter(user=user)
        return Lesson.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_lessons = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_lessons, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Операция создания недоступна."},
                        status=403)

    def perform_update(self, serializer):
        # Логика для обновления урока
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Операция удаления недоступна."},
                        status=403)


class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(description__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context
