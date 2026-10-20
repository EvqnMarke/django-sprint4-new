from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from core.constants import POSTS_BY_PAGE
from .models import Post


def get_published_posts(
        queryset=None, filter_published=True, annotate_comments=True,
):
    if queryset is None:
        queryset = Post.objects.all()

    queryset = queryset.select_related('category', 'location', 'author')

    if filter_published:
        queryset = queryset.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )

    if annotate_comments:
        queryset = queryset.annotate(comment_count=Count('comments'))

    return queryset.order_by('-pub_date')


def get_paginated_page(request, posts_list):
    paginator = Paginator(posts_list, POSTS_BY_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
