from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from fabric_bolt.core import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('fabric_bolt.accounts.urls')),
    url(r'^$', views.Dashboard.as_view(), name='index'),
    url(r'^hosts/', include('fabric_bolt.hosts.urls')),
    url(r'^projects/', include('fabric_bolt.projects.urls')),
)

#Serve the static files from django
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
