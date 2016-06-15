from django.conf.urls import include, url
from django.contrib import admin
import home.views

urlpatterns = [
    # General
    url(r'^$', home.views.index, name='index'),
    url(r'^ama/(?P<ama_id>[0-9]+)/$', home.views.detail, name='detail'),
    url(r'^ama/(?P<ama_id>[0-9]+)/question/$', home.views.question, name='question'),

    # Accounts
    url(r'^login/$', home.views.login, name='login'),
    url(r'^logout/$', home.views.logout, name='logout'),
    url(r'^signup/$', home.views.signup, name='signup'),

    # Creation
    url(r'^create/$', home.views.createama, name='createama'),

    url(r'^admin/', admin.site.urls),
]
