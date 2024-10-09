from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    """Model for course"""
    title = models.CharField(max_length=255, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """Model for lesson"""
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью урока', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
