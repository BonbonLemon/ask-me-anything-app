from django.conf.urls import include, url
from django.contrib import admin

from home.api.amas.views import (
    AMACreateAPIView,
    AMAListAPIView,
    AMADetailAPIView,
    AMADeleteAPIView,
    AMAUpdateAPIView,
    )

urlpatterns = [
    url(r'^$', AMAListAPIView.as_view(), name='list'),
    url(r'^create/$', AMACreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', AMADetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/delete/$', AMADeleteAPIView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/update/$', AMAUpdateAPIView.as_view(), name='update'),
]
