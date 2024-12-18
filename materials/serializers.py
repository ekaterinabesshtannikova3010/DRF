from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'



    class Meta:
        model = Course
        fields = '__all__'  # или укажите конкретные поля, включая 'lesson_count'

    def get_lesson_count(self, obj):
        return obj.lessons.count()