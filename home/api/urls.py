from django.conf.urls import include, url
from django.contrib import admin

from home.api.views import (
    AMACreateAPIView,
    AMAListAPIView,
    AMADetailAPIView,
    AMADeleteAPIView,
    AMAUpdateAPIView,
    )

urlpatterns = [
    url(r'^amas/$', AMAListAPIView.as_view(), name='ama-list'),
    url(r'^amas/create/$', AMACreateAPIView.as_view(), name='ama-create'),
    url(r'^amas/(?P<pk>\d+)/$', AMADetailAPIView.as_view(), name='ama-detail'),
    url(r'^amas/(?P<pk>\d+)/delete/$', AMADeleteAPIView.as_view(), name='ama-delete'),
    url(r'^amas/(?P<pk>\d+)/update/$', AMAUpdateAPIView.as_view(), name='ama-update'),
]
