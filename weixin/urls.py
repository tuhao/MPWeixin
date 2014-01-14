from django.conf.urls import patterns, include, url
from signature.views import *
from approve.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import os

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weixin.views.home', name='home'),
    # url(r'^weixin/', include('weixin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$',check_signature),
    url(r'^detail/(?P<msg_id>\d+)/$',news_detail),

    url(r'^approve/$',approve),
    
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.dirname(globals()["__file__"])+'/static'}),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.dirname(globals()["__file__"])+ '/media'}),
)
