from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from blog.models import Post
from core.constants import POSTS_BY_PAGE


def get_published_posts(
        queryset=None, filter_published=True, annotate_comments=True,
):
    queryset = queryset or Post.objects.all()
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


def get_paginated_page(request, posts_list, per_page=POSTS_BY_PAGE):
    paginator = Paginator(posts_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
