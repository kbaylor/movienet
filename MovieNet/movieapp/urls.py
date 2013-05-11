from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from movieapp import views

urlpatterns = patterns('',
<<<<<<< HEAD
    # ex: /movie/
    url(r'^$', views.index, name='index'),
    # ex: /movie/5/
    url(r'^movie/(?P<movieid>\d+)/$', views.movie, name='movie'),
    # ex: /actor/5/
    url(r'^actor/(?P<actorid>\d+)/$', views.actor, name='actor'),
    # ex: /director/5
    url(r'^director/(?P<did>\d+)/$', views.director, name='director'),
    url(r'^find/$', views.find),
    
=======
    # ex: /movieapp
    url(r'^$', TemplateView.as_view(template_name = 'base.html'), name='index'),
    # ex: /movieapp/add
    url(r'add$', views.add_movie, name='add_movie'),
>>>>>>> 1a2ae7f... Authentication done. along with some other stuff
)