from django.conf.urls import include, url
from django.contrib import admin
import home.views

urlpatterns = [
    url(r'^$', home.views.index, name='index'),
    url(r'^ama/(?P<ama_id>[0-9]+)/$', home.views.detail, name='detail'),

    url(r'^admin/', admin.site.urls),
]
