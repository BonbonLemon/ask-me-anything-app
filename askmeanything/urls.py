from django.conf.urls import include, url
from django.contrib import admin
import home.views

from home.views import IndexListView

urlpatterns = [
    # AMA
    url(r'^$', IndexListView.as_view(), name='index'),
    url(r'^ama/(?P<ama_id>[0-9]+)/$', home.views.detail, name='ama_detail'),
    url(r'^ama/(?P<ama_id>[0-9]+)/question/$', home.views.ask_question, name='question'),
    url(r'^ama/(?P<ama_id>[0-9]+)/question/(?P<question_id>[0-9]+)/$', home.views.question, name='question_detail'),
    url(r'^ama/create/$', home.views.createama, name='createama'),

    # Accounts
    url(r'^login/$', home.views.login, name='login'),
    url(r'^logout/$', home.views.logout, name='logout'),
    url(r'^signup/$', home.views.signup, name='signup'),

    # Creation

    url(r'^admin/', admin.site.urls),
]
