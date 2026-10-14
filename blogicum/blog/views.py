from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import Http404
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count


from .models import Category, Post, Comment
from .forms import PostForm, CommentForm


POSTS_BY_PAGE = 10


def get_published_posts():
    return (
        Post.objects.select_related('category', 'location', 'author')
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )


def index(request):
    template_name = 'blog/index.html'
    posts_list = get_published_posts()
    paginator = Paginator(posts_list, POSTS_BY_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


def post_detail(request, id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post, pk=id)

    if not (
        post.is_published
        and post.category.is_published
        and post.pub_date <= timezone.now()
    ):
        if post.author != request.user:
            raise Http404()

    comments = post.comments.all()

    context = {
        'post': post,
        'form': CommentForm(),
        'comments': comments,
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts_list = get_published_posts().filter(category=category)
    paginator = Paginator(posts_list, POSTS_BY_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        post = self.get_object()
        return redirect('blog:post_detail', id=post.pk)


class OnlyCommentAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def handle_no_permission(self):
        comment = self.get_object()
        return redirect('blog:post_detail', id=comment.post.id)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class PostUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'id': self.object.pk})


class PostDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_obj = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def form_invalid(self, form):
        context = {
            'post': self.post_obj,
            'form': form,
            'comments': self.post_obj.comments.all(),
        }
        return render(self.request, 'blog/detail.html', context)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.post_obj.pk})


class CommentUpdateView(
    LoginRequiredMixin,
    OnlyCommentAuthorMixin,
    UpdateView,
):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['post_id'])
        comment = self.get_object()
        if comment.post.id != kwargs['post_id']:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'id': self.object.post.id},
        )


class CommentDeleteView(
    LoginRequiredMixin,
    OnlyCommentAuthorMixin,
    DeleteView,
):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['post_id'])
        comment = self.get_object()
        if comment.post.id != kwargs['post_id']:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'id': self.object.post.id},
        )
