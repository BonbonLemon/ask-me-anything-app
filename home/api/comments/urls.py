from django.conf.urls import include, url
from django.contrib import admin

from home.api.comments.views import (
    # CommentCreateAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    # CommentDeleteAPIView,
    # CommentUpdateAPIView,
    )

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='detail'),
    # url(r'^amas/$', CommentListAPIView.as_view(), name='ama-list'),
    # url(r'^amas/create/$', CommentCreateAPIView.as_view(), name='ama-create'),
    # url(r'^amas/(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='ama-detail'),
    # url(r'^amas/(?P<pk>\d+)/delete/$', CommentDeleteAPIView.as_view(), name='ama-delete'),
    # url(r'^amas/(?P<pk>\d+)/update/$', CommentUpdateAPIView.as_view(), name='ama-update'),
]
