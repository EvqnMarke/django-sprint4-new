from django.urls import path

from users.views import ProfileListView, ProfileUpdateView
from .views import (
    CommentCreateView, CommentDeleteView, CommentUpdateView,
    PostCreateView, PostDeleteView, PostUpdateView,
    category_posts, index, post_detail,
)

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path(
        'category/<slug:category_slug>/',
        category_posts,
        name='category_posts',
    ),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/',
         PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/',
         PostDeleteView.as_view(),
         name='delete_post'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', ProfileListView.as_view(), name='profile'),
    path('posts/<int:post_id>/comment/',
         CommentCreateView.as_view(),
         name='add_comment'),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        CommentDeleteView.as_view(),
        name='delete_comment',
    ),
]
