from textwrap import shorten
from django.db import models
from django.contrib.auth import get_user_model
from core.models import PublishedModel


User = get_user_model()


MAX_LENGHT_CHARFIELD = 256
SHORT_TITLE_LENGTH = 30


class Category(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGHT_CHARFIELD,
        verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta(PublishedModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return shorten(self.title, SHORT_TITLE_LENGTH, placeholder='...')


class Location(PublishedModel):
    name = models.CharField(
        max_length=MAX_LENGHT_CHARFIELD,
        verbose_name='Название места')

    class Meta(PublishedModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return shorten(self.name, SHORT_TITLE_LENGTH, placeholder='...')


class Post(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGHT_CHARFIELD,
        verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='post_images/',
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return shorten(self.title, SHORT_TITLE_LENGTH, placeholder='...')


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)
        default_related_name = 'comments'

    def __str__(self):
        return shorten(self.text, SHORT_TITLE_LENGTH, placeholder='...')
