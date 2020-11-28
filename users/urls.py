from django.urls import path
from .views import (SignUpView, follow, TweetUserListView, CommentUserListView,
                    FollowerUserListView, FollowingUserListView)

app_name = 'users'
urlpatterns = [
    path('singup/', SignUpView.as_view(), name='signup'),
    path('follow/', follow, name='follow'),
    path(
        'userlist/tweet/<int:pk>/',
        TweetUserListView.as_view(),
        name='tweet_user_list'
    ),
    path(
        'userlist/comment/<int:pk>/',
        CommentUserListView.as_view(),
        name='comment_user_list'
    ),
    path(
        'userlist/follower/<int:pk>/',
        FollowerUserListView.as_view(),
        name='follower_user_list'
    ),
    path(
        'userlist/following/<int:pk>/',
        FollowingUserListView.as_view(),
        name='following_user_list'
    ),
]
