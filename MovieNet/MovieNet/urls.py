from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from registration.views import register, user_profile


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MovieNet.views.home', name='home'),
    # url(r'^MovieNet/', include('MovieNet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^$', login, {'template_name':'registration/login.html'}),
     url(r'^login$', login, {'template_name':'registration/login.html'}),
     url(r'^logout', logout, {'next_page': '/login'}),
     url(r'^account$', user_profile),
     url(r'^register$', register),
     url(r'^movieapp/', include('movieapp.urls'))
)
