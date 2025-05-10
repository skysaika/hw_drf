from rest_framework.pagination import PageNumberPagination



class CoursePaginator(PageNumberPagination):
    """Пагинатор для курса"""
    page_size = 2

class LessonPaginator(CoursePaginator):
    """Пагинатор для уроков"""
    page_size = 5

class PaymentPaginator(CoursePaginator):
    """Пагинатор для списка платежей"""