from django.conf.urls import include, url
from django.contrib import admin
import home.views

urlpatterns = [
    url(r'^$', home.views.home),
    url(r'^admin/', admin.site.urls),
]
