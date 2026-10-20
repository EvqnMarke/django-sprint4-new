from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'slug',
        'is_published',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'get_image',
        'title',
        'pub_date',
        'author',
        'category',
        'location',
        'is_published',
    )
    list_editable = (
        'category',
        'location',
        'is_published',
    )
    search_fields = (
        'title',
        'text',
    )
    list_filter = (
        'category',
        'pub_date',
    )
    list_display_links = ('title',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'text', 'image'),
        }),
        ('Информация об авторе и связях', {
            'fields': ('author', 'category', 'location'),
        }),
        ('Даты и публикация', {
            'fields': ('pub_date', 'is_published'),
        }),
    )

    @admin.display(description='Изображение')
    def get_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="50" '
                f'height="50" style="object-fit: cover;">',
            )
        return None


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
        'created_at',
    )

    search_fields = (
        'text',
        'author__username',
        'post__title',
    )

    list_filter = ('created_at',)
