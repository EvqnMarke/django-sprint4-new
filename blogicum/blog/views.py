from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView

from blog.forms import CommentForm, PostForm
from blog.mixins import OnlyAuthorMixin, OnlyCommentAuthorMixin
from blog.models import Category, Comment, Post
from blog.services import get_paginated_page, get_published_posts


def index(request):
    posts_list = get_published_posts()
    page_obj = get_paginated_page(request, posts_list)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if not (
        post.is_published
        and post.category.is_published
        and post.pub_date <= timezone.now()
    ) and post.author != request.user:
        raise Http404()

    comments = post.comments.select_related('author')

    context = {
        'post': post,
        'form': CommentForm(),
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts_list = get_published_posts(queryset=category.posts.all())
    page_obj = get_paginated_page(request, posts_list)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class PostUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class PostDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        post_obj = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = post_obj
        return super().form_valid(form)

    def form_invalid(self, form):
        post_obj = get_object_or_404(Post, pk=self.kwargs['post_id'])
        context = {
            'post': post_obj,
            'form': form,
            'comments': post_obj.comments.select_related('author'),
        }
        return render(self.request, 'blog/detail.html', context)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']},
        )


class CommentUpdateView(
    LoginRequiredMixin,
    OnlyCommentAuthorMixin,
    UpdateView,
):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.id},
        )


class CommentDeleteView(
    LoginRequiredMixin,
    OnlyCommentAuthorMixin,
    DeleteView,
):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.id},
        )
