from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

import home.views

from home.views import AMAListView, AMADetailView, AMACreateView, UserFormView, SessionFormView, LogoutView

urlpatterns = [
    # AMA
    url(r'^$', AMAListView.as_view(), name='index'),
    url(r'^ama/create/$', AMACreateView.as_view(), name='createama'),
    url(r'^ama/(?P<pk>[0-9]+)/$', AMADetailView.as_view(), name='ama_detail'),
    url(r'^ama/(?P<ama_id>[0-9]+)/question/$', home.views.ask_question, name='question'),
    url(r'^ama/(?P<ama_id>[0-9]+)/question/(?P<question_id>[0-9]+)/$', home.views.question, name='question_detail'),

    # API
    url(r'^api/', include("home.api.urls", namespace='apis')),

    # Questions
    # url(r'questions/', home.views.QuestionList.as_view()),

    # Accounts
    url(r'^login/$', SessionFormView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^signup/$', UserFormView.as_view(), name='signup'),

    # Creation

    url(r'^admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)
