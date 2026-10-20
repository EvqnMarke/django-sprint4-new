from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, UpdateView

from blog.models import Post
from blog.services import get_published_posts
from core.constants import POSTS_BY_PAGE
from .forms import ProfileForm

User = get_user_model()


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'page_obj'
    paginate_by = POSTS_BY_PAGE

    def get_queryset(self):
        self.profile_user = get_object_or_404(
            User,
            username=self.kwargs['username'],
        )

        return get_published_posts(
            queryset=self.profile_user.posts.all(),
            filter_published=(self.profile_user != self.request.user),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile_user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )
