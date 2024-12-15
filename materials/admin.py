from django.contrib import admin
from .models import Course, Lesson

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1  # Количество дополнительных пустых форм для добавления новых уроков

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
