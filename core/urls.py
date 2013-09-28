from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'', views.Dashboard.as_view, name='dashboard_view'),
    url(r'^hosts/', include('hosts.urls')),

)

#Serve the static files from django
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
