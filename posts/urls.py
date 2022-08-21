from django.urls import path

from .views import (CommentDeleteView, PostDeleteView, PostUpdateView,
                    switch_like, post_comment_create_and_list_view)

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main-post-view'),
    path('like/', switch_like, name='switch-like-view'),

    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<pk>/comment_delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
