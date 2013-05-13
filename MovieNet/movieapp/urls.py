from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from movieapp import views

urlpatterns = patterns('',
    # ex: /movieapp
    url(r'^$', TemplateView.as_view(template_name = 'base.html'), name='index'),
    # ex: /movieapp/add
    url(r'add$', views.add_movie, name='add_movie'),
    # ex: /movie/5/
    url(r'movie/(?P<movieid>\d+)/$', views.movie, name='movie'),
    # ex: /actor/5/
    url(r'actor/(?P<actorid>\d+)/$', views.actor, name='actor'),
    # ex: /director/5
    url(r'^director/(?P<did>\d+)/$', views.director, name='director'),
    url(r'^find/$', views.find),
    url(r'^movies/top/$', views.top_movies),
    url(r'^users/top/$', views.top_users),
    
    url(r'^find/advanced/$', views.advancedfind),

)