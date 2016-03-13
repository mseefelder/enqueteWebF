from django.conf.urls import url, include

#   For authentication we import this
#   For each authentication view, follow the documentation:
# https://docs.djangoproject.com/en/1.9/topics/auth/default/#all-authentication-views
#   Login url below serves as an example. The parameter 'template_name' is passed to
# make this view load 'enquetes/login.html' on our templates folder. The default would be
# 'registration/login.html' on our templates folder
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

app_name = 'enquetes'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>[0-9]+)/$', views.AnswerView.as_view(), name='answer'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url('^', include('django.contrib.auth.urls')),
    #url(r'^register/$', views.register, name='register'), #Previous wy used to register, was buggy
    #below, there's the way using built-in forms
    url('^register/', CreateView.as_view(template_name='registration/register.html', form_class=UserCreationForm, success_url='/enquetes'), name='resgister'),
    #url(r'^login/$', auth_views.login, {'template_name': 'enquetes/login.html'}, name='login'),
    #url(r'^logout/$', auth_views.logout, {'template_name': 'enquetes/logout.html'}, name='logout'),
]

