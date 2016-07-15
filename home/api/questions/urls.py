from django.conf.urls import include, url
from django.contrib import admin

from home.api.questions.views import (
    # QuestionCreateAPIView,
    QuestionListAPIView,
    QuestionDetailAPIView,
    # QuestionDeleteAPIView,
    # QuestionUpdateAPIView,
    )

urlpatterns = [
    url(r'^$', QuestionListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', QuestionDetailAPIView.as_view(), name='detail'),
    # url(r'^amas/$', QuestionListAPIView.as_view(), name='ama-list'),
    # url(r'^amas/create/$', QuestionCreateAPIView.as_view(), name='ama-create'),
    # url(r'^amas/(?P<pk>\d+)/$', QuestionDetailAPIView.as_view(), name='ama-detail'),
    # url(r'^amas/(?P<pk>\d+)/delete/$', QuestionDeleteAPIView.as_view(), name='ama-delete'),
    # url(r'^amas/(?P<pk>\d+)/update/$', QuestionUpdateAPIView.as_view(), name='ama-update'),
]
