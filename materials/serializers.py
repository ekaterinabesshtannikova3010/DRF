from rest_framework import serializers
from .validators import LinkValidator
from users.models import Payment
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    video_link = serializers.URLField(validators=[LinkValidator(field='video_link')])

    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_link']
        validators = [LinkValidator(field='video_link')]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'lesson_count']

    def get_lesson_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

