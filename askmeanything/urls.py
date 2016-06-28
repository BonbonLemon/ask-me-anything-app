from django.conf.urls import include, url
from django.contrib import admin
import home.views

from home.views import AMAListView, AMADetailView, UserFormView

urlpatterns = [
    # AMA
    url(r'^$', AMAListView.as_view(), name='index'),
    url(r'^ama/(?P<pk>[0-9]+)/$', AMADetailView.as_view(), name='ama_detail'),
    url(r'^ama/(?P<ama_id>[0-9]+)/question/$', home.views.ask_question, name='question'),
    url(r'^ama/(?P<ama_id>[0-9]+)/question/(?P<question_id>[0-9]+)/$', home.views.question, name='question_detail'),
    url(r'^ama/create/$', home.views.createama, name='createama'),

    # Accounts
    url(r'^login/$', home.views.vlogin, name='login'),
    url(r'^logout/$', home.views.vlogout, name='logout'),
    url(r'^signup/$', UserFormView.as_view(), name='signup'),

    # Creation

    url(r'^admin/', admin.site.urls),
]
