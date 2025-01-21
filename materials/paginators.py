from rest_framework.pagination import PageNumberPagination

class LessonsPagination(PageNumberPagination):
    page_size = 10  # Количество уроков на странице
    page_size_query_param = 'page_size'  # Параметр для указания количества элементов на странице
    max_page_size = 100  # Максимально допустимое количество элементов на странице

class CoursesPagination(PageNumberPagination):
    page_size = 5  # Количество курсов на странице
    page_size_query_param = 'page_size'  # Параметр для указания количества элементов на странице
    max_page_size = 50  # Максимально допустимое количество элементов на странице