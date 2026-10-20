from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from blog.models import Post


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        post = self.get_object()
        return redirect('blog:post_detail', post_id=post.pk)


class OnlyCommentAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        comment = self.get_object()
        get_object_or_404(
            Post,
            pk=self.request.resolver_match.kwargs['post_id'],
        )
        if comment.post.id != self.request.resolver_match.kwargs['post_id']:
            raise Http404()
        return comment.author == self.request.user

    def handle_no_permission(self):
        comment = self.get_object()
        return redirect('blog:post_detail', post_id=comment.post.id)
