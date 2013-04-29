from django.conf.urls import patterns, url

from movieapp import views

urlpatterns = patterns('',
    # ex: /movie/
    url(r'^$', views.index, name='index'),
    # ex: /movie/5/
    url(r'^(?P<movieid>\d+)/$', views.movie, name='movie'),
    # ex: /actor/5/
    url(r'^(?P<actorid>\d+)/$', views.actor, name='actor'),
    # ex: /director/5
    url(r'^(?P<did>\d+)/$', views.director, name='director'),
)