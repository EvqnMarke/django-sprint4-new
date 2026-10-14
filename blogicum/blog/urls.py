from django.urls import path
from . import views


from .views import (
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)
from users.views import ProfileListView, ProfileUpdateView


app_name = 'blog'


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(),
         name='delete_post'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', ProfileListView.as_view(), name='profile'),
    path('posts/<int:pk>/comment/', CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         CommentDeleteView.as_view(), name='delete_comment'),
]
