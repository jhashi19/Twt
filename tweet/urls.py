from django.urls import path
from .views import (TwtListView, TwtDetailView, TwtDeleteView, TwtCreateView,
                    TwtCommentCreateView)


app_name = 'tweet'
urlpatterns = [
    path('list/', TwtListView.as_view(), name='twt_list'),
    path('detail/<int:pk>/', TwtDetailView.as_view(), name='twt_detail'),
    path('delete/<int:pk>/', TwtDeleteView.as_view(), name='twt_delete'),
    path('create/', TwtCreateView.as_view(), name='twt_create'),
    path('comment/create/<int:pk>', TwtCommentCreateView.as_view(),
         name='comment_create'),
]
