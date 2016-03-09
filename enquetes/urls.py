from django.conf.urls import url

from . import views

app_name = 'enquetes'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<question_id>[0-9]+)/answer/$', views.answer, name='answer'),
        url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
        url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]

