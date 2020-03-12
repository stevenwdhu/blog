from django.urls import path, include
from .views import PostComment

app_name = 'comment'

urlpatterns = [
    path('<int:article_id>/post-comment/', PostComment.as_view(), name='post_comment'),
    path('<int:article_id>/post-comment/<int:parent_id>', PostComment.as_view(), name='comment_reply'),
    ]
